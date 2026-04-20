import pathlib
import unittest


class TestPackagingFiles(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(__file__).resolve().parents[1]

    def test_bat_has_inno_overrides(self):
        content = (self.root / "build_installer.bat").read_text(encoding="utf-8")
        self.assertIn("/DMyAppVersion=%APP_VERSION%", content)
        self.assertIn("/DMyAppPublisher=\"%APP_PUBLISHER%\"", content)
        self.assertIn("/DMyAppURL=%APP_URL%", content)

    def test_iss_uses_preprocessor_defaults(self):
        content = (self.root / "installer" / "StandaloneMacro.iss").read_text(encoding="utf-8")
        self.assertIn("#ifndef MyAppVersion", content)
        self.assertIn("AppPublisherURL={#MyAppURL}", content)
        self.assertIn("Source: \"..\\dist\\StandaloneMacro.exe\"", content)

    def test_windows_ci_workflow_exists(self):
        workflow = self.root / ".github" / "workflows" / "build-windows.yml"
        self.assertTrue(workflow.exists())
        content = workflow.read_text(encoding="utf-8")
        self.assertIn("runs-on: windows-latest", content)
        self.assertIn("actions/upload-artifact@v4", content)

    def test_release_workflow_exists(self):
        workflow = self.root / ".github" / "workflows" / "release-windows.yml"
        self.assertTrue(workflow.exists())
        content = workflow.read_text(encoding="utf-8")
        self.assertIn("softprops/action-gh-release@v2", content)
        self.assertIn("installer/output/StandaloneMacroSetup.exe", content)


if __name__ == "__main__":
    unittest.main()
