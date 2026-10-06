from level1.task_1_file_organizer.file_organizer import organize_directory

def test_organizes_files(tmp_path):
    (tmp_path / "photo.jpg").write_text("x", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("y", encoding="utf-8")
    log = tmp_path / "organization_log.csv"

    count = organize_directory(tmp_path, log)

    assert count == 2
    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert (tmp_path / "Documents" / "notes.txt").exists()
    assert log.exists()
