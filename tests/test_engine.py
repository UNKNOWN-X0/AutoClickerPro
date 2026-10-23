"""Engine regression tests without GUI imports or real input events."""
import importlib
import sys
import types
import unittest
from unittest.mock import Mock, patch

# Substitute only the device boundary; engine and state are the real modules.
devices = types.ModuleType('autoclicker.dependencies')
devices.pyautogui = Mock()
with patch.dict(sys.modules, {'autoclicker.dependencies': devices}):
    engine = importlib.import_module('autoclicker.engine')
state = engine.state


class EngineTests(unittest.TestCase):
    def setUp(self):
        state.running = True
        state.click_count = 0
        devices.pyautogui.reset_mock(side_effect=True)
        self.counter = Mock()
        self.refresh = Mock()
        self.cfg = dict(mode='Fixed', repeat_n=3, button='Left', action='Single',
                        interval=0.1, rand_min=0, rand_max=0, use_multipoint=False,
                        points=[], rand_pos=False)

    def run_loop(self):
        with patch.object(engine.time, 'sleep'):
            engine.click_loop(self.cfg, self.counter, self.refresh)

    def test_fixed_count_and_callbacks(self):
        self.run_loop()
        self.assertEqual(state.click_count, 3)
        self.assertEqual(devices.pyautogui.click.call_count, 3)
        self.assertEqual(self.counter.call_count, 3)
        self.assertFalse(state.running)
        self.refresh.assert_called_once_with()

    def test_points_cycle_and_double_click(self):
        self.cfg.update(use_multipoint=True, points=[(10,20),(30,40)], action='Double')
        self.run_loop()
        self.assertEqual([c.args[:2] for c in devices.pyautogui.moveTo.call_args_list],
                         [(10,20),(30,40),(10,20)])
        self.assertEqual(devices.pyautogui.doubleClick.call_count, 3)

    def test_device_error_stops_and_refreshes(self):
        devices.pyautogui.click.side_effect = RuntimeError('failsafe')
        self.run_loop()
        self.assertEqual(state.click_count, 0)
        self.assertFalse(state.running)
        self.refresh.assert_called_once_with()

    def test_stopped_loop_never_clicks(self):
        state.running = False
        self.run_loop()
        devices.pyautogui.click.assert_not_called()

    def test_macro_repeats_preserve_timing_and_keys(self):
        events=[dict(type='click', time=0, button='Right', x=1, y=2),
                dict(type='key', time=0.25, key='a')]
        with patch.object(engine.time, 'sleep') as sleep:
            engine.macro_replay(events, 2, False, self.counter, self.refresh)
        self.assertEqual(state.click_count, 2)
        self.assertEqual(devices.pyautogui.press.call_count, 2)
        devices.pyautogui.press.assert_called_with('a')
        self.assertEqual([c.args for c in sleep.call_args_list], [(0.25,), (0.25,)])
        self.assertFalse(state.running)
        self.refresh.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
