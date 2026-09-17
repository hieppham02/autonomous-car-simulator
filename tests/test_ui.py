"""Kiểm tra sự kiện thật và các pha mô phỏng với Pygame headless."""

import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import src.renderer as ui

from src.benchmark import BenchmarkRunner
from src.main import Application
from src.map_model import GridMap
from src.renderer import (
    BLACK, GRID_AREA, INSET, Renderer, grid_geometry,
    grid_panel_geometry, grid_position, window_viewport,
)
from src.simulation import Simulation


class SimulationTests(unittest.TestCase):
    def test_scan_finishes_before_car_moves_and_trail_is_kept(self):
        grid = GridMap(3, 3)
        grid.start, grid.goal = (0, 0), (2, 2)
        for algorithm in ("BFS", "Dijkstra", "A*"):
            with self.subTest(algorithm=algorithm):
                sim = Simulation(grid)
                sim.start(grid, algorithm, 0)
                now = 0
                while sim.phase == "scanning":
                    now += 15
                    sim.update(now, 10, scan_batch=1)
                    self.assertEqual(sim.car_position, grid.start)
                    self.assertFalse(sim.visible_path)
                self.assertEqual(sim.metrics["position"], grid.goal)
                for _ in range(len(sim.path)):
                    now += 10
                    sim.update(now, 10)
                self.assertEqual(sim.phase, "done")
                self.assertEqual(sim.car_position, grid.goal)
                self.assertEqual(sim.visible_path, set(sim.path))

    def test_no_path_and_start_equals_goal(self):
        grid = GridMap(2, 2)
        grid.start, grid.goal = (0, 0), (1, 1)
        grid.obstacles.update({(1, 0), (0, 1)})
        sim = Simulation(grid)
        sim.start(grid, "BFS", 0)
        sim.update(20, 10)
        self.assertEqual(sim.phase, "done")
        self.assertIsNone(sim.cost)
        self.assertFalse(sim.visible_path)
        grid.goal = grid.start
        sim.start(grid, "A*", 20)
        sim.update(40, 10)
        sim.update(60, 10)
        self.assertEqual(sim.phase, "done")
        self.assertEqual(sim.cost, 0)

    def test_benchmark_uses_snapshot_and_reports_failure(self):
        grid = GridMap(2, 2)
        grid.start, grid.goal = (0, 0), (1, 1)
        runner = BenchmarkRunner(grid, repetitions=2)
        grid.obstacles.update({(1, 0), (0, 1)})
        while not runner.done:
            runner.step()
        self.assertTrue(all(r["cost"] == 2 for r in runner.results))
        blocked = BenchmarkRunner(grid, repetitions=1)
        while not blocked.done:
            blocked.step()
        self.assertTrue(all(not r["found"] and r["cost"] is None
                            and r["path_length"] is None for r in blocked.results))


class InterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))
        cls.renderer = Renderer()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.app = Application()
        self.app.grid.start = (0, 7)
        self.app.grid.goal = (20, 29)
        self.app.simulation.reset(self.app.grid)
        self.canvas = pygame.Surface(ui.layout_size())
        self.viewport = window_viewport((1200, 760), ui.layout_size())

    def click(self, position, button=1, now=0):
        logical_width, logical_height = ui.layout_size()
        self.viewport = window_viewport((1200, 760), ui.layout_size())
        x = self.viewport.x + round(
            position[0] * self.viewport.width / logical_width
        )
        y = self.viewport.y + round(
            position[1] * self.viewport.height / logical_height
        )
        self.app.handle_event(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(x, y), button=button),
            self.viewport, now,
        )

    def test_benchmark_button_runs_three_and_edit_invalidates(self):
        self.click(self.app.controls["benchmark"].center)
        self.assertIsNotNone(self.app.benchmark)
        self.assertEqual(self.app.simulation.phase, "idle")
        phases = {name: [] for name in ("BFS", "Dijkstra", "A*")}
        for frame in range(5000):
            self.app.update(frame * 50)
            sim = self.app.simulation
            if sim.algorithm and (not phases[sim.algorithm]
                                  or phases[sim.algorithm][-1] != sim.phase):
                phases[sim.algorithm].append(sim.phase)
            if self.app.benchmark.done:
                break
            self.assertEqual(self.app.benchmark.results, [])
        self.assertTrue(self.app.benchmark.done)
        for sequence in phases.values():
            self.assertEqual(sequence, ["scanning", "moving", "done"])
        results = self.app.benchmark.results
        self.assertEqual([r["algorithm"] for r in results], ["BFS", "Dijkstra", "A*"])
        self.assertTrue(all(r["cost"] == 42 and r["nodes"] > 0 for r in results))
        self.renderer.draw(self.canvas, self.app.grid, self.app.simulation,
                           self.app.path_step_delay, self.app.benchmark)
        cell_width, cell_height, grid_rect = grid_geometry(self.app.grid)
        self.click((grid_rect.x + cell_width / 2,
                    grid_rect.y + cell_height / 2))
        self.assertIn((0, 0), self.app.grid.obstacles)
        self.assertIsNone(self.app.benchmark)

    def test_benchmark_can_be_cancelled_by_edit_or_algorithm(self):
        for action in ("clear", "random", "BFS"):
            self.click(self.app.controls["benchmark"].center)
            self.app.update(20)
            self.click(self.app.controls[action].center, now=30)
            self.assertIsNone(self.app.benchmark)

    def test_benchmark_finishes_when_no_route_exists(self):
        self.app.grid.obstacles.update({(0, 6), (0, 8), (1, 7)})
        self.click(self.app.controls["benchmark"].center)
        for frame in range(5000):
            self.app.update(frame * 50)
            if self.app.benchmark.done:
                break
        self.assertTrue(self.app.benchmark.done)
        self.assertTrue(all(not result["found"] for result in self.app.benchmark.results))
        self.assertFalse(self.app.simulation.visible_path)

    def test_resized_clicks_controls_and_restart(self):
        self.click(self.app.controls["increase"].center)
        self.assertEqual(self.app.path_step_delay, 60)
        self.click(self.app.controls["decrease"].center)
        self.assertEqual(self.app.path_step_delay, 50)
        for name in ("BFS", "Dijkstra", "A*"):
            self.click(self.app.controls[name].center)
            self.assertEqual(self.app.simulation.algorithm, name)
            self.assertEqual(self.app.simulation.phase, "scanning")
            self.app.update(20)
            self.renderer.draw(self.canvas, self.app.grid, self.app.simulation,
                               self.app.path_step_delay, self.app.benchmark)
        self.click(self.app.controls["clear"].center)
        self.assertEqual(self.app.simulation.phase, "idle")
        self.assertFalse(self.app.grid.obstacles)
        self.assertFalse(self.app.simulation.scanned_cells)
        self.click(self.app.controls["random"].center)
        self.assertTrue(self.app.grid.obstacles)
        _, _, grid_rect = grid_geometry(self.app.grid)
        self.assertIsNone(grid_position((grid_rect.x - 1, grid_rect.y), self.app.grid))
        self.assertIsNone(grid_position((grid_rect.x, grid_rect.y - 1), self.app.grid))

    def test_custom_grid_inputs_validation_and_creation(self):
        self.click(self.app.controls["rows_input"].center)
        self.assertTrue(self.app.input_select_all)
        for digit in "12":
            self.app.handle_event(
                pygame.event.Event(pygame.KEYDOWN, key=ord(digit), unicode=digit),
                self.viewport, 0,
            )
        self.click(self.app.controls["columns_input"].center)
        self.assertTrue(self.app.input_select_all)
        for digit in "18":
            self.app.handle_event(
                pygame.event.Event(pygame.KEYDOWN, key=ord(digit), unicode=digit),
                self.viewport, 0,
            )
        self.click(self.app.controls["apply_grid"].center)
        self.assertEqual((self.app.grid.rows, self.app.grid.columns), (12, 18))
        self.assertEqual(self.app.grid.start, (0, 0))
        self.assertEqual(self.app.grid.goal, (11, 17))
        self.assertEqual(self.app.simulation.car_position, (0, 0))
        self.app.grid_inputs["rows"] = "4"
        self.app.create_custom_grid()
        self.assertTrue(self.app.grid_message.startswith("Lỗi"))
        self.assertEqual((self.app.grid.rows, self.app.grid.columns), (12, 18))

        self.app.grid_inputs = {"rows": "50", "columns": "50"}
        self.app.create_custom_grid()
        cell_width, cell_height, rect = grid_geometry(self.app.grid)
        self.assertGreater(cell_width, 0)
        self.assertGreater(cell_height, 0)
        self.assertLessEqual(rect.width, GRID_AREA.width)
        self.assertLessEqual(rect.height, GRID_AREA.height)

    def test_grid_cells_stay_square_for_different_dimensions(self):
        for rows, columns in ((5, 80), (50, 5), (25, 50), (50, 50)):
            self.app.grid_inputs = {
                "rows": str(rows), "columns": str(columns),
            }
            self.app.create_custom_grid()
            cell_width, cell_height, rect = grid_geometry(self.app.grid)
            self.assertGreater(cell_width, 0)
            self.assertGreater(cell_height, 0)
            self.assertLessEqual(rect.width, GRID_AREA.width)
            self.assertLessEqual(rect.height, GRID_AREA.height)
            panel = grid_panel_geometry(self.app.grid)
            self.assertGreaterEqual(panel.width, rect.width + 28)
            self.assertEqual(panel.top, ui.CONTENT_TOP)
            self.assertEqual(panel.bottom, ui.HEIGHT - ui.MARGIN)
            self.assertEqual(panel.centerx, rect.centerx)
            self.assertGreaterEqual(rect.top - panel.top, 14)

    def test_reset_preserves_start_and_goal(self):
        self.app.grid.start = (3, 4)
        self.app.grid.goal = (20, 40)
        self.app.grid.obstacles.update({(5, 5), (6, 6)})
        self.app.grid.set_weight((7, 7), 4)
        self.click(self.app.controls["clear"].center)
        self.assertEqual(self.app.grid.start, (3, 4))
        self.assertEqual(self.app.grid.goal, (20, 40))
        self.assertFalse(self.app.grid.obstacles)
        self.assertFalse(self.app.grid.weights)

    def test_user_can_place_start_and_goal(self):
        cell_width, cell_height, rect = grid_geometry(self.app.grid)

        def center(row, column):
            return (rect.x + (column + 0.5) * cell_width,
                    rect.y + (row + 0.5) * cell_height)

        self.app.grid.obstacles.update({(3, 4), (20, 40)})
        self.click(self.app.controls["set_start"].center)
        self.assertEqual(self.app.edit_mode, "start")
        self.click(center(3, 4))
        self.assertEqual(self.app.grid.start, (3, 4))
        self.assertNotIn((3, 4), self.app.grid.obstacles)
        self.assertEqual(self.app.edit_mode, "obstacle")

        self.click(self.app.controls["set_goal"].center)
        self.click(center(20, 40))
        self.assertEqual(self.app.grid.goal, (20, 40))
        self.assertNotIn((20, 40), self.app.grid.obstacles)
        self.assertEqual(self.app.simulation.car_position, (3, 4))

        self.click(self.app.controls["set_start"].center)
        self.click(center(20, 40))
        self.assertTrue(self.app.grid_message.startswith("Lỗi"))
        self.assertEqual(self.app.grid.start, (3, 4))

    def test_render_preserves_obstacle_seam_and_loads_car(self):
        self.app.grid.obstacles.update({(0, 0), (0, 1)})
        self.renderer.draw(self.canvas, self.app.grid, self.app.simulation,
                           self.app.path_step_delay, None)
        cell_width, cell_height, grid_rect = grid_geometry(self.app.grid)
        boundary = grid_rect.x + round(cell_width)
        for x in (boundary - 1, boundary):
            self.assertEqual(self.canvas.get_at((x, grid_rect.y + 5))[:3], BLACK)
        car_size = round(min(cell_width, cell_height))
        car_images = self.renderer.car_images(car_size)
        self.assertEqual(len(car_images), 4)
        for sprite in car_images.values():
            self.assertLessEqual(max(sprite.get_size()), car_size)
            self.assertTrue(sprite.get_flags() & pygame.SRCALPHA)

    def test_empty_benchmark_card_keeps_its_content_area(self):
        self.renderer.draw(self.canvas, self.app.grid, self.app.simulation,
                           self.app.path_step_delay, None)
        self.assertEqual(
            self.canvas.get_at((ui.RIGHT_X + 30, 450))[:3],
            INSET,
        )
