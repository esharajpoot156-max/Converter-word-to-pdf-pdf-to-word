from pathlib import Path
import flet as ft
from api import convert_file

PRIMARY = ft.Colors.BLUE  # change to PURPLE, GREEN, TEAL, etc.

MODES = {
    "word_to_pdf": {"label": "Word → PDF", "ext": ["doc", "docx"], "out": ".pdf"},
    "pdf_to_word": {"label": "PDF → Word", "ext": ["pdf"], "out": ".docx"},
}

NO_FILE_TEXT = "Click to select a file"


def unique_path(folder, stem, ext):
    path = folder / (stem + ext)
    i = 1
    while path.exists():
        path = folder / f"{stem} ({i}){ext}"
        i += 1
    return path


def main(page: ft.Page):
    page.title = "Word ⇄ PDF Converter"
    page.theme = ft.Theme(color_scheme_seed=PRIMARY)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 520
    page.window.height = 680

    state = {"mode": "word_to_pdf", "path": None}

    # ---------- UI pieces ----------
    drop_icon = ft.Icon(ft.Icons.UPLOAD_FILE, size=48, color=PRIMARY)
    file_text = ft.Text(NO_FILE_TEXT, size=15, text_align=ft.TextAlign.CENTER)
    hint_text = ft.Text("Allowed: .doc, .docx", size=12, opacity=0.6)

    progress = ft.ProgressBar(visible=False, color=PRIMARY)

    status_text = ft.Text(size=14)
    status_box = ft.Container(
        content=status_text,
        visible=False,
        padding=14,
        border_radius=12,
        width=380,
    )

    convert_btn = ft.FilledButton(
        "Convert",
        icon=ft.Icons.AUTORENEW,
        disabled=True,
        width=380,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
    )

    theme_btn = ft.IconButton(ft.Icons.DARK_MODE, tooltip="Toggle theme")

    # ---------- helpers ----------
    def show_status(message, kind):
        color = ft.Colors.GREEN if kind == "success" else ft.Colors.RED
        status_text.value = message
        status_text.color = color
        status_box.bgcolor = ft.Colors.with_opacity(0.12, color)
        status_box.visible = True

    def hide_status():
        status_box.visible = False

    def reset_file():
        state["path"] = None
        file_text.value = NO_FILE_TEXT
        drop_icon.name = ft.Icons.UPLOAD_FILE
        convert_btn.disabled = True

    # ---------- events ----------
    def on_mode_change(e):
        state["mode"] = list(e.control.selected)[0]
        reset_file()
        hide_status()
        exts = ", ".join("." + x for x in MODES[state["mode"]]["ext"])
        hint_text.value = f"Allowed: {exts}"
        page.update()

    def on_pick(e: ft.FilePickerResultEvent):
        if e.files:
            state["path"] = e.files[0].path
            file_text.value = e.files[0].name
            drop_icon.name = ft.Icons.DESCRIPTION
            convert_btn.disabled = False
            hide_status()
        page.update()

    picker = ft.FilePicker(on_result=on_pick)
    page.overlay.append(picker)

    def pick_click(e):
        picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=MODES[state["mode"]]["ext"],
        )

    def convert_click(e):
        mode = state["mode"]
        src = Path(state["path"])

        convert_btn.disabled = True
        progress.visible = True
        hide_status()
        page.update()

        ok, result = convert_file(mode, src.name, src.read_bytes())

        if ok:
            downloads = Path.home() / "Downloads"
            downloads.mkdir(exist_ok=True)
            out = unique_path(downloads, src.stem, MODES[mode]["out"])
            out.write_bytes(result)
            show_status(f"Done! Saved to:\n{out}", "success")
        else:
            show_status(result, "error")

        progress.visible = False
        convert_btn.disabled = False
        page.update()

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_btn.icon = ft.Icons.LIGHT_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_btn.icon = ft.Icons.DARK_MODE
        page.update()

    convert_btn.on_click = convert_click
    theme_btn.on_click = toggle_theme

    # ---------- layout ----------
    drop_area = ft.Container(
        content=ft.Column(
            [drop_icon, file_text, hint_text],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        width=380,
        padding=30,
        border=ft.border.all(2, PRIMARY),
        border_radius=16,
        bgcolor=ft.Colors.with_opacity(0.05, PRIMARY),
        on_click=pick_click,
        ink=True,
        alignment=ft.alignment.center,
    )

    header = ft.Row(
        [
            ft.Row(
                [
                    ft.Icon(ft.Icons.SWAP_HORIZ, color=PRIMARY, size=30),
                    ft.Text("Converter", size=24, weight=ft.FontWeight.BOLD),
                ]
            ),
            theme_btn,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        width=380,
    )

    mode_switch = ft.SegmentedButton(
        selected={"word_to_pdf"},
        on_change=on_mode_change,
        segments=[
            ft.Segment(value=k, label=ft.Text(v["label"]))
            for k, v in MODES.items()
        ],
    )

    card = ft.Container(
        content=ft.Column(
            [header, mode_switch, drop_area, convert_btn, progress, status_box],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=30,
        border_radius=24,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
        ),
    )

    page.add(card)


ft.app(target=main)