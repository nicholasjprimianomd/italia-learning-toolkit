from __future__ import annotations

import asyncio
import random

import flet as ft

from app.chat_client import ChatClient, ChatClientError, ChatMessage
from config import OPENAI_API_KEY
from data import (
    ARTICLE_OPTIONS,
    ARTICLE_QUESTIONS,
    BODY_OPTIONS,
    BODY_QUESTIONS,
    CLOTHING_OPTIONS,
    CLOTHING_QUESTIONS,
    COLOR_OPTIONS,
    COLOR_QUESTIONS,
    DAY_MONTH_OPTIONS,
    DAY_MONTH_QUESTIONS,
    FAMILY_OPTIONS,
    FAMILY_QUESTIONS,
    GREETING_OPTIONS,
    GREETING_QUESTIONS,
    PIACERE_OPTIONS,
    PIACERE_QUESTIONS,
    POSSESSIVE_OPTIONS,
    POSSESSIVE_QUESTIONS,
    PREPOSITION_QUESTIONS,
    PRONUNCIATION_OPTIONS,
    PRONUNCIATION_QUESTIONS,
    QUESTION_WORD_OPTIONS,
    QUESTION_WORD_QUESTIONS,
    REFERENCE_SECTIONS,
    SpacedRepetitionSystem,
    TIME_OPTIONS,
    TIME_QUESTIONS,
    VERB_OPTIONS,
    VERB_QUESTIONS,
    WEATHER_OPTIONS,
    WEATHER_QUESTIONS,
)

SIDEBAR_BG = "#1f2530"
CARD_BG = "#151b24"
CHAT_PANEL_BG = "#1c2230"
ASSISTANT_BUBBLE_BG = "#1f2530"


def safe_update(*controls: ft.Control | None) -> None:
    for control in controls:
        if control is not None and getattr(control, "page", None):
            control.update()


async def get_user_id(page: ft.Page) -> str:
    """Get user ID from storage."""
    try:
        user_id = await page.client_storage.get_async("user_id") or ""
        return str(user_id) if user_id else ""
    except Exception:
        return ""


async def set_user_id(page: ft.Page, user_id: str) -> None:
    """Save user ID to storage."""
    try:
        await page.client_storage.set_async("user_id", user_id)
    except Exception:
        pass


async def load_progress(page: ft.Page, key: str) -> tuple[int, int]:
    """Load saved progress from client storage and cloud."""
    user_id = await get_user_id(page)
    
    # Try cloud first if user_id is set
    if user_id:
        try:
            from progress_api import load_progress_cloud
            cloud_score, cloud_total = await load_progress_cloud(user_id, key)
            if cloud_total > 0:
                return cloud_score, cloud_total
        except Exception:
            pass
    
    # Fall back to local storage
    try:
        score = await page.client_storage.get_async(f"{key}_score") or 0
        total = await page.client_storage.get_async(f"{key}_total") or 0
        return int(score), int(total)
    except Exception:
        return 0, 0


async def save_progress(page: ft.Page, key: str, score: int, total: int) -> None:
    """Save progress to client storage and cloud."""
    # Save locally first
    try:
        await page.client_storage.set_async(f"{key}_score", score)
        await page.client_storage.set_async(f"{key}_total", total)
    except Exception:
        pass
    
    # Also save to cloud if user_id is set
    user_id = await get_user_id(page)
    if user_id:
        try:
            from progress_api import save_progress_cloud
            await save_progress_cloud(user_id, key, score, total)
        except Exception:
            pass  # Silently fail if cloud unavailable


class ReferenceView:
    def __init__(self, page: ft.Page, chat_client: ChatClient) -> None:
        self.page = page
        self.chat_client = chat_client
        self.selected_index = 0
        self.topic_tiles: list[ft.ListTile] = []
        self.title_text = ft.Text(
            REFERENCE_SECTIONS[self.selected_index]["title"],
            weight=ft.FontWeight.BOLD,
            size=20,
            color=ft.Colors.WHITE,
        )
        self.reference_text = ft.Text(
            REFERENCE_SECTIONS[self.selected_index]["content"],
            selectable=True,
            size=13,
            no_wrap=False,
            color=ft.Colors.WHITE,
        )
        self.explanation_text = ft.Text("", size=12, color=ft.Colors.BLUE_200, italic=True)
        self.explain_button = ft.ElevatedButton(
            "Explain selected text",
            icon="lightbulb",
            on_click=self._on_explain_selection,
            visible=False,
        )
        self.view = self._build()

    def _build(self) -> ft.Control:
        self.topic_tiles = [self._build_tile(i, section["title"]) for i, section in enumerate(REFERENCE_SECTIONS)]

        sidebar = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Topics", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.WHITE),
                    ft.Divider(height=1),
                    ft.Column(
                        controls=self.topic_tiles,
                        spacing=2,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=10,
            bgcolor=SIDEBAR_BG,
            border_radius=8,
        )

        content_panel = ft.Container(
            content=ft.Column(
                [
                    self.title_text,
                    ft.Divider(),
                    ft.TextField(
                        value="",
                        hint_text="Select text in the reference below, then click 'Explain'",
                        multiline=True,
                        min_lines=1,
                        max_lines=2,
                        on_change=self._on_selection_change,
                        read_only=False,
                    ) if False else ft.Container(),  # Hidden selection input
                    self.reference_text,
                    self.explain_button,
                    self.explanation_text,
                ],
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            bgcolor=CARD_BG,
            border_radius=8,
            padding=15,
            expand=True,
        )

        # Add text selection listener
        self.reference_text.on_focus = self._on_text_focus
        self.reference_text.on_blur = self._on_text_blur

        return ft.ResponsiveRow(
            controls=[
                ft.Column([sidebar], col={"xs": 12, "sm": 12, "md": 4, "lg": 3}),
                ft.Column([content_panel], col={"xs": 12, "sm": 12, "md": 8, "lg": 9}, expand=True),
            ],
            expand=True,
        )

    def _build_tile(self, index: int, title: str) -> ft.ListTile:
        return ft.ListTile(
            title=ft.Text(title, color=ft.Colors.WHITE),
            selected=index == self.selected_index,
            on_click=lambda _: self._select_topic(index),
        )

    def _select_topic(self, index: int) -> None:
        self.selected_index = index
        for i, tile in enumerate(self.topic_tiles):
            tile.selected = i == index
            safe_update(tile)

        section = REFERENCE_SECTIONS[index]
        self.title_text.value = section["title"]
        self.reference_text.value = section["content"]
        safe_update(self.title_text, self.reference_text)

    def prime(self) -> None:
        safe_update(self.title_text, self.reference_text, *self.topic_tiles)

    def _on_text_focus(self, e: ft.ControlEvent) -> None:
        """Show explain button when text is focused."""
        self.explain_button.visible = True
        safe_update(self.explain_button)

    def _on_text_blur(self, e: ft.ControlEvent) -> None:
        """Keep button visible even when focus is lost."""
        pass

    def _on_selection_change(self, e: ft.ControlEvent) -> None:
        """Handle text selection changes."""
        pass

    def _on_explain_selection(self, e: ft.ControlEvent) -> None:
        """Get ChatGPT explanation for selected text."""
        # Since Flet doesn't support getting selected text directly,
        # we'll use a dialog to let users paste the text they want explained
        self.selected_text_field = ft.TextField(
            multiline=True,
            min_lines=2,
            max_lines=5,
            autofocus=True,
        )
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Explain Italian Text"),
            content=ft.Column(
                [
                    ft.Text("Paste or type the Italian text you want explained:"),
                    self.selected_text_field,
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self._close_dialog()),
                ft.ElevatedButton("Explain", on_click=lambda _: self.page.run_task(self._explain_text)),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def _close_dialog(self) -> None:
        """Close the dialog."""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    async def _explain_text(self) -> None:
        """Get explanation from ChatGPT."""
        selected_text = self.selected_text_field.value.strip()
        if not selected_text:
            self.explanation_text.value = "Please enter some text to explain."
            safe_update(self.explanation_text)
            return

        self._close_dialog()

        # Show loading state
        self.explanation_text.value = "Getting explanation from ChatGPT..."
        self.explanation_text.color = ft.Colors.BLUE_200
        safe_update(self.explanation_text)

        try:
            # Call ChatGPT to explain the text
            messages = [
                ChatMessage(
                    role="system",
                    content="You are an Italian language tutor. Provide concise explanations of Italian words, phrases, or grammar concepts. Focus on meaning, usage, and any important grammatical notes."
                ),
                ChatMessage(
                    role="user",
                    content=f"Explain this Italian text or concept: {selected_text}"
                )
            ]

            response = await self.chat_client.chat(messages, model="gpt-4o-mini")
            self.explanation_text.value = f"💡 {response}"
            self.explanation_text.color = ft.Colors.GREEN_200
        except ChatClientError as error:
            self.explanation_text.value = f"Error: {error}"
            self.explanation_text.color = ft.Colors.RED_400
        except Exception as error:
            self.explanation_text.value = f"Unexpected error: {error}"
            self.explanation_text.color = ft.Colors.RED_400

        safe_update(self.explanation_text)


class ArticleExerciseView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.questions = ARTICLE_QUESTIONS
        self.options = ARTICLE_OPTIONS
        self.storage_key = "article_exercise"

        self.current: dict[str, str] | None = None
        self.score = 0
        self.total = 0
        
        # Load saved progress
        page.run_task(self._load_progress)

        self.prompt_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
        self.option_group = ft.RadioGroup(
            content=ft.Column(
                controls=[ft.Radio(value=option, label=option) for option in self.options],
                spacing=8,
            )
        )
        self.feedback_text = ft.Text("", size=14)
        self.explanation_text = ft.Text("", size=13, color=ft.Colors.ON_SURFACE_VARIANT)
        self.score_text = ft.Text("Score: 0 / 0", weight=ft.FontWeight.BOLD)

        actions = ft.Row(
            [
                ft.ElevatedButton("Check answer", icon="check_circle", on_click=self._on_check_answer),
                ft.OutlinedButton("New question", icon="refresh", on_click=self._on_new_question),
                ft.OutlinedButton("Reset progress", icon="restart_alt", on_click=self._on_reset_progress),
            ],
            spacing=8,
            wrap=True,
        )

        self.view = ft.Column(
            [
                ft.Text("Pick the correct definite article", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Match the article to gender, number, and sound.", size=14, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Divider(),
                self.prompt_text,
                self.option_group,
                actions,
                self.feedback_text,
                self.explanation_text,
                ft.Divider(height=24),
                self.score_text,
            ],
            spacing=16,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        self._load_new_question()

    def _load_new_question(self) -> None:
        self.current = random.choice(self.questions)
        prompt = (
            f"Which article matches {self.current['english']}? "
            f"({self.current['italian']} • {self.current['number']} {self.current['gender']})"
        )
        self.prompt_text.value = prompt

        self.option_group.value = None

        self.feedback_text.value = ""

        self.explanation_text.value = ""

        safe_update(self.prompt_text, self.option_group, self.feedback_text, self.explanation_text)

        self._update_score_text()

    def _on_new_question(self, _: ft.ControlEvent) -> None:
        self._load_new_question()

    def _on_check_answer(self, _: ft.ControlEvent) -> None:
        if not self.option_group.value:
            self._show_snack_bar("Select an article before checking.")
            return

        assert self.current is not None
        choice = self.option_group.value

        self.total += 1
        is_correct = choice == self.current["correct"]

        if is_correct:
            self.score += 1
            self.feedback_text.value = "✔ Correct!"
            self.feedback_text.color = ft.Colors.GREEN_400
        else:
            self.feedback_text.value = f"✘ Not quite. The correct article is {self.current['correct']}."
            self.feedback_text.color = ft.Colors.RED_400

        self.explanation_text.value = self.current["explanation"]

        safe_update(self.feedback_text, self.explanation_text)

        self._update_score_text()
        # Save progress
        self.page.run_task(self._save_progress)

        # Auto-advance to next question if correct
        if is_correct:
            self.page.run_task(self._auto_advance)

    async def _auto_advance(self) -> None:
        """Auto-advance to next question after a short delay."""
        await asyncio.sleep(1.2)
        self._load_new_question()

    async def _load_progress(self) -> None:
        """Load saved progress from storage."""
        score, total = await load_progress(self.page, self.storage_key)
        self.score = score
        self.total = total
        self._update_score_text()

    async def _save_progress(self) -> None:
        """Save current progress to storage."""
        await save_progress(self.page, self.storage_key, self.score, self.total)

    def _on_reset_progress(self, _: ft.ControlEvent) -> None:
        """Reset progress to zero."""
        self.score = 0
        self.total = 0
        self._update_score_text()
        self.page.run_task(self._save_progress)
        self._show_snack_bar("Progress reset!")

    def _update_score_text(self) -> None:
        if self.total == 0:
            self.score_text.value = "Score: 0 / 0"
        else:
            percent = (self.score / self.total) * 100
            self.score_text.value = f"Score: {self.score} / {self.total} ({percent:.0f}%)"
        safe_update(self.score_text)

    def _show_snack_bar(self, message: str) -> None:
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()


class VerbExerciseView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.questions = VERB_QUESTIONS
        self.options = VERB_OPTIONS
        self.storage_key = "verb_exercise"

        self.current: dict[str, str] | None = None
        self.score = 0
        self.total = 0
        
        # Load saved progress
        page.run_task(self._load_progress)

        self.prompt_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
        self.option_group = ft.RadioGroup(
            content=ft.Column(
                controls=[ft.Radio(value=option, label=option) for option in self.options],
                spacing=8,
            )
        )
        self.feedback_text = ft.Text("", size=14)
        self.explanation_text = ft.Text("", size=13, color=ft.Colors.ON_SURFACE_VARIANT)
        self.score_text = ft.Text("Score: 0 / 0", weight=ft.FontWeight.BOLD)

        actions = ft.Row(
            [
                ft.ElevatedButton("Check answer", icon="check_circle", on_click=self._on_check_answer),
                ft.OutlinedButton("New question", icon="refresh", on_click=self._on_new_question),
                ft.OutlinedButton("Reset progress", icon="restart_alt", on_click=self._on_reset_progress),
            ],
            spacing=8,
            wrap=True,
        )

        self.view = ft.Column(
            [
                ft.Text("Match verbs with pronouns", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Decide whether the sentence needs essere, stare, or avere — then pick the right conjugation.",
                    size=14,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Divider(),
                self.prompt_text,
                self.option_group,
                actions,
                self.feedback_text,
                self.explanation_text,
                ft.Divider(height=24),
                self.score_text,
            ],
            spacing=16,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        self._load_new_question()

    def _load_new_question(self) -> None:
        self.current = random.choice(self.questions)
        prompt = (
            f"Select the correct form of '{self.current['verb']}' for pronoun '{self.current['pronoun']}' "
            f"({self.current['english']})."
        )
        self.prompt_text.value = prompt

        self.option_group.value = None

        self.feedback_text.value = ""

        self.explanation_text.value = ""

        safe_update(self.prompt_text, self.option_group, self.feedback_text, self.explanation_text)

        self._update_score_text()

    def _on_new_question(self, _: ft.ControlEvent) -> None:
        self._load_new_question()

    def _on_check_answer(self, _: ft.ControlEvent) -> None:
        if not self.option_group.value:
            self._show_snack_bar("Select a verb form before checking.")
            return

        assert self.current is not None
        choice = self.option_group.value

        self.total += 1
        is_correct = choice == self.current["correct"]

        if is_correct:
            self.score += 1
            self.feedback_text.value = "✔ Correct!"
            self.feedback_text.color = ft.Colors.GREEN_400
        else:
            self.feedback_text.value = f"✘ Not quite. The correct form is '{self.current['correct']}'."
            self.feedback_text.color = ft.Colors.RED_400

        self.explanation_text.value = self.current["explanation"]
        safe_update(self.feedback_text, self.explanation_text)

        self._update_score_text()
        # Save progress
        self.page.run_task(self._save_progress)

        # Auto-advance to next question if correct
        if is_correct:
            self.page.run_task(self._auto_advance)

    async def _auto_advance(self) -> None:
        """Auto-advance to next question after a short delay."""
        await asyncio.sleep(1.2)
        self._load_new_question()

    async def _load_progress(self) -> None:
        """Load saved progress from storage."""
        score, total = await load_progress(self.page, self.storage_key)
        self.score = score
        self.total = total
        self._update_score_text()

    async def _save_progress(self) -> None:
        """Save current progress to storage."""
        await save_progress(self.page, self.storage_key, self.score, self.total)

    def _on_reset_progress(self, _: ft.ControlEvent) -> None:
        """Reset progress to zero."""
        self.score = 0
        self.total = 0
        self._update_score_text()
        self.page.run_task(self._save_progress)
        self._show_snack_bar("Progress reset!")

    def _update_score_text(self) -> None:
        if self.total == 0:
            self.score_text.value = "Score: 0 / 0"
        else:
            percent = (self.score / self.total) * 100
            self.score_text.value = f"Score: {self.score} / {self.total} ({percent:.0f}%)"
        safe_update(self.score_text)

    def _show_snack_bar(self, message: str) -> None:
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()


class PrepositionExerciseView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.questions = PREPOSITION_QUESTIONS
        self.storage_key = "preposition_exercise"

        self.current: dict[str, str] | None = None
        self.score = 0
        self.total = 0
        
        # Load saved progress
        page.run_task(self._load_progress)

        self.prompt_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
        self.options_column = ft.Column(spacing=8)
        self.option_group = ft.RadioGroup(content=self.options_column)
        self.feedback_text = ft.Text("", size=14)
        self.explanation_text = ft.Text("", size=13, color=ft.Colors.ON_SURFACE_VARIANT)
        self.score_text = ft.Text("Score: 0 / 0", weight=ft.FontWeight.BOLD)

        actions = ft.Row(
            [
                ft.ElevatedButton("Check answer", icon="check_circle", on_click=self._on_check_answer),
                ft.OutlinedButton("New question", icon="refresh", on_click=self._on_new_question),
                ft.OutlinedButton("Reset progress", icon="restart_alt", on_click=self._on_reset_progress),
            ],
            spacing=8,
            wrap=True,
        )

        self.view = ft.Column(
            [
                ft.Text("Combine prepositions and articles", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Choose the correct fused form (preposizione articolata) for the prompt.",
                    size=14,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Divider(),
                self.prompt_text,
                self.option_group,
                actions,
                self.feedback_text,
                self.explanation_text,
                ft.Divider(height=24),
                self.score_text,
            ],
            spacing=16,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        self._load_new_question()

    def _load_new_question(self) -> None:
        self.current = random.choice(self.questions)
        prompt = (
            f"Combine '{self.current['preposition']}' with '{self.current['article_phrase']}' "
            f"({self.current['english']})."
        )
        self.prompt_text.value = prompt

        choices = {self.current["result"]}
        while len(choices) < min(4, len(self.questions)):
            choices.add(random.choice(self.questions)["result"])
        options = list(choices)
        random.shuffle(options)

        self.options_column.controls = [ft.Radio(value=option, label=option) for option in options]
        self.option_group.value = None

        self.feedback_text.value = ""

        self.explanation_text.value = ""

        safe_update(self.prompt_text, self.options_column, self.option_group, self.feedback_text, self.explanation_text)

        self._update_score_text()

    def _on_new_question(self, _: ft.ControlEvent) -> None:
        self._load_new_question()

    def _on_check_answer(self, _: ft.ControlEvent) -> None:
        if not self.option_group.value:
            self._show_snack_bar("Select an option before checking.")
            return

        assert self.current is not None
        choice = self.option_group.value

        self.total += 1
        is_correct = choice == self.current["result"]

        if is_correct:
            self.score += 1
            self.feedback_text.value = "✔ Correct!"
            self.feedback_text.color = ft.Colors.GREEN_400
        else:
            self.feedback_text.value = f"✘ Not quite. The correct form is '{self.current['result']}'."
            self.feedback_text.color = ft.Colors.RED_400

        self.explanation_text.value = self.current["explanation"]
        safe_update(self.feedback_text, self.explanation_text)

        self._update_score_text()
        # Save progress
        self.page.run_task(self._save_progress)

        # Auto-advance to next question if correct
        if is_correct:
            self.page.run_task(self._auto_advance)

    async def _auto_advance(self) -> None:
        """Auto-advance to next question after a short delay."""
        await asyncio.sleep(1.2)
        self._load_new_question()

    async def _load_progress(self) -> None:
        """Load saved progress from storage."""
        score, total = await load_progress(self.page, self.storage_key)
        self.score = score
        self.total = total
        self._update_score_text()

    async def _save_progress(self) -> None:
        """Save current progress to storage."""
        await save_progress(self.page, self.storage_key, self.score, self.total)

    def _on_reset_progress(self, _: ft.ControlEvent) -> None:
        """Reset progress to zero."""
        self.score = 0
        self.total = 0
        self._update_score_text()
        self.page.run_task(self._save_progress)
        self._show_snack_bar("Progress reset!")

    def _update_score_text(self) -> None:
        if self.total == 0:
            self.score_text.value = "Score: 0 / 0"
        else:
            percent = (self.score / self.total) * 100
            self.score_text.value = f"Score: {self.score} / {self.total} ({percent:.0f}%)"
        safe_update(self.score_text)

    def _show_snack_bar(self, message: str) -> None:
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()


class GenericExerciseView:
    """Generic exercise view for simple question-answer format."""

    def __init__(self, page: ft.Page, title: str, subtitle: str, questions: list[dict], options: list[str],
                 storage_key: str, question_key: str = "question", answer_key: str = "correct") -> None:
        self.page = page
        self.questions = questions
        self.options = options
        self.storage_key = storage_key
        self.question_key = question_key
        self.answer_key = answer_key

        self.current: dict[str, str] | None = None
        self.score = 0
        self.total = 0

        # Load saved progress
        page.run_task(self._load_progress)

        self.prompt_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
        self.option_group = ft.RadioGroup(
            content=ft.Column(
                controls=[ft.Radio(value=option, label=option) for option in self.options],
                spacing=8,
            )
        )
        self.feedback_text = ft.Text("", size=14)
        self.explanation_text = ft.Text("", size=13, color=ft.Colors.ON_SURFACE_VARIANT)
        self.score_text = ft.Text("Score: 0 / 0", weight=ft.FontWeight.BOLD)

        actions = ft.Row(
            [
                ft.ElevatedButton("Check answer", icon="check_circle", on_click=self._on_check_answer),
                ft.OutlinedButton("New question", icon="refresh", on_click=self._on_new_question),
                ft.OutlinedButton("Reset progress", icon="restart_alt", on_click=self._on_reset_progress),
            ],
            spacing=8,
            wrap=True,
        )

        self.view = ft.Column(
            [
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                ft.Text(subtitle, size=14, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Divider(),
                self.prompt_text,
                self.option_group,
                actions,
                self.feedback_text,
                self.explanation_text,
                ft.Divider(height=24),
                self.score_text,
            ],
            spacing=16,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        self._load_new_question()

    def _load_new_question(self) -> None:
        self.current = random.choice(self.questions)
        # Support different keys for different question types
        if self.question_key in self.current:
            self.prompt_text.value = self.current[self.question_key]
        elif "situation" in self.current:
            self.prompt_text.value = self.current["situation"]
        elif "meaning" in self.current:
            self.prompt_text.value = f"What is the Italian word for: {self.current['meaning']}?"
        elif "time" in self.current:
            self.prompt_text.value = f"How do you say '{self.current['time']}' in Italian?"
        elif "english" in self.current:
            self.prompt_text.value = f"Translate to Italian: {self.current['english']}"
        elif "noun_phrase" in self.current:
            self.prompt_text.value = f"What is the correct color form for: {self.current['noun_phrase']}?"

        self.option_group.value = None
        self.feedback_text.value = ""
        self.explanation_text.value = ""

        safe_update(self.prompt_text, self.option_group, self.feedback_text, self.explanation_text)
        self._update_score_text()

    def _on_new_question(self, _: ft.ControlEvent) -> None:
        self._load_new_question()

    def _on_check_answer(self, _: ft.ControlEvent) -> None:
        if not self.option_group.value:
            self._show_snack_bar("Select an option before checking.")
            return

        assert self.current is not None
        choice = self.option_group.value
        correct_answer = self.current[self.answer_key]

        self.total += 1
        is_correct = choice == correct_answer

        if is_correct:
            self.score += 1
            self.feedback_text.value = "✔ Correct!"
            self.feedback_text.color = ft.Colors.GREEN_400
        else:
            self.feedback_text.value = f"✘ Not quite. The correct answer is '{correct_answer}'."
            self.feedback_text.color = ft.Colors.RED_400

        self.explanation_text.value = self.current["explanation"]
        safe_update(self.feedback_text, self.explanation_text)

        self._update_score_text()
        # Save progress
        self.page.run_task(self._save_progress)

        # Auto-advance to next question if correct
        if is_correct:
            self.page.run_task(self._auto_advance)

    async def _auto_advance(self) -> None:
        """Auto-advance to next question after a short delay."""
        await asyncio.sleep(1.2)
        self._load_new_question()

    async def _load_progress(self) -> None:
        """Load saved progress from storage."""
        score, total = await load_progress(self.page, self.storage_key)
        self.score = score
        self.total = total
        self._update_score_text()

    async def _save_progress(self) -> None:
        """Save current progress to storage."""
        await save_progress(self.page, self.storage_key, self.score, self.total)

    def _on_reset_progress(self, _: ft.ControlEvent) -> None:
        """Reset progress to zero."""
        self.score = 0
        self.total = 0
        self._update_score_text()
        self.page.run_task(self._save_progress)
        self._show_snack_bar("Progress reset!")

    def _update_score_text(self) -> None:
        if self.total == 0:
            self.score_text.value = "Score: 0 / 0"
        else:
            percent = (self.score / self.total) * 100
            self.score_text.value = f"Score: {self.score} / {self.total} ({percent:.0f}%)"
        safe_update(self.score_text)

    def _show_snack_bar(self, message: str) -> None:
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()


class CombinedReviewView:
    """Combined review using spaced repetition across all topics."""

    # All question sets with their topic names
    ALL_QUESTION_SETS = {
        "Articles": ARTICLE_QUESTIONS,
        "Body Parts": BODY_QUESTIONS,
        "Clothing": CLOTHING_QUESTIONS,
        "Colors": COLOR_QUESTIONS,
        "Days & Months": DAY_MONTH_QUESTIONS,
        "Family": FAMILY_QUESTIONS,
        "Greetings": GREETING_QUESTIONS,
        "Piacere & Mancare": PIACERE_QUESTIONS,
        "Possessive Pronouns": POSSESSIVE_QUESTIONS,
        "Prepositions": PREPOSITION_QUESTIONS,
        "Pronunciation": PRONUNCIATION_QUESTIONS,
        "Question Words": QUESTION_WORD_QUESTIONS,
        "Time": TIME_QUESTIONS,
        "Verbs": VERB_QUESTIONS,
        "Weather": WEATHER_QUESTIONS,
    }

    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.srs = SpacedRepetitionSystem()

        # Build question database with IDs
        self.all_questions = []
        self.question_map = {}  # Maps question_id to (topic, question_dict)

        for topic_name, questions in self.ALL_QUESTION_SETS.items():
            for idx, question in enumerate(questions):
                question_id = f"{topic_name}:{idx}"
                self.all_questions.append(question_id)
                self.question_map[question_id] = (topic_name, question)

        self.current_question_id = None
        self.current_question = None
        self.current_topic = None
        self.due_questions = []

        # Load SRS data
        page.run_task(self._load_srs_data)

        # UI Components
        self.topic_label = ft.Text("", size=12, color=ft.Colors.BLUE_400, weight=ft.FontWeight.BOLD)
        self.prompt_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
        self.answer_field = ft.TextField(
            label="Your answer",
            autofocus=True,
            on_submit=lambda _: self._on_check_answer(None),
        )
        self.feedback_text = ft.Text("", size=14)
        self.explanation_text = ft.Text("", size=13, color=ft.Colors.ON_SURFACE_VARIANT)

        # Statistics
        self.overall_stats_text = ft.Text("", size=14)
        self.topic_stats_container = ft.Column([], spacing=4)
        self.due_count_text = ft.Text("", size=14, color=ft.Colors.ORANGE_400)

        # Actions
        actions = ft.Row(
            [
                ft.ElevatedButton("Check answer", icon="check_circle", on_click=self._on_check_answer),
                ft.OutlinedButton("Skip", icon="skip_next", on_click=self._on_skip),
                ft.OutlinedButton("Refresh stats", icon="refresh", on_click=self._on_refresh_stats),
            ],
            spacing=8,
            wrap=True,
        )

        # Stats section (collapsible)
        self.stats_expanded = ft.ExpansionPanelList(
            controls=[
                ft.ExpansionPanel(
                    header=ft.Text("Statistics", weight=ft.FontWeight.BOLD),
                    content=ft.Container(
                        content=ft.Column(
                            [
                                self.overall_stats_text,
                                ft.Divider(height=12),
                                ft.Text("Topic Breakdown:", weight=ft.FontWeight.BOLD, size=13),
                                self.topic_stats_container,
                            ],
                            spacing=8,
                        ),
                        padding=10,
                    ),
                    can_tap_header=True,
                )
            ]
        )

        self.view = ft.Column(
            [
                ft.Text("Combined Review", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Intelligent spaced repetition across all topics", size=14, color=ft.Colors.ON_SURFACE_VARIANT),
                self.due_count_text,
                ft.Divider(),
                self.topic_label,
                self.prompt_text,
                self.answer_field,
                actions,
                self.feedback_text,
                self.explanation_text,
                ft.Divider(height=24),
                self.stats_expanded,
            ],
            spacing=16,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        # Load first question after data is loaded
        page.run_task(self._initialize_review)

    async def _initialize_review(self) -> None:
        """Initialize the review session after SRS data is loaded."""
        await asyncio.sleep(0.1)  # Wait for SRS data to load
        self._load_next_due_question()
        self._update_stats()

    def _load_next_due_question(self) -> None:
        """Load the next question that is due for review."""
        # Get due questions
        self.due_questions = self.srs.get_due_questions(self.all_questions, limit=50)

        if not self.due_questions:
            self.prompt_text.value = "No questions due for review! Check back later."
            self.answer_field.visible = False
            self.topic_label.value = ""
            safe_update(self.prompt_text, self.answer_field, self.topic_label)
            return

        # Get the most urgent question
        self.current_question_id = self.due_questions[0]
        self.current_topic, self.current_question = self.question_map[self.current_question_id]

        # Update UI
        self.topic_label.value = f"Topic: {self.current_topic}"
        self._format_question_prompt()
        self.answer_field.value = ""
        self.answer_field.visible = True
        self.feedback_text.value = ""
        self.explanation_text.value = ""

        # Update due count
        due_count = sum(1 for qid in self.due_questions if
                       self.srs.get_question_record(qid)["next_review"] <=
                       self.srs.records.get(qid, {}).get("next_review", "9999"))
        self.due_count_text.value = f"📚 {len(self.due_questions)} questions in queue ({due_count} due now)"

        safe_update(self.topic_label, self.prompt_text, self.answer_field,
                   self.feedback_text, self.explanation_text, self.due_count_text)

    def _format_question_prompt(self) -> None:
        """Format the question prompt based on question type."""
        q = self.current_question

        if "question" in q:
            self.prompt_text.value = q["question"]
        elif "situation" in q:
            self.prompt_text.value = q["situation"]
        elif "meaning" in q:
            self.prompt_text.value = f"What is the Italian word for: {q['meaning']}?"
        elif "time" in q:
            self.prompt_text.value = f"How do you say '{q['time']}' in Italian?"
        elif "english" in q:
            self.prompt_text.value = f"Translate to Italian: {q['english']}"
        elif "noun_phrase" in q:
            self.prompt_text.value = f"What is the correct color form for: {q['noun_phrase']}?"
        else:
            self.prompt_text.value = str(q)

    def _get_correct_answer(self) -> str:
        """Get the correct answer from the current question."""
        q = self.current_question
        if "correct" in q:
            return q["correct"]
        elif "answer" in q:
            return q["answer"]
        elif "response" in q:
            return q["response"]
        return ""

    def _on_check_answer(self, _: ft.ControlEvent | None) -> None:
        """Check the user's answer and update SRS."""
        if not self.answer_field.value or not self.answer_field.value.strip():
            self._show_snack_bar("Please enter an answer.")
            return

        user_answer = self.answer_field.value.strip().lower()
        correct_answer = self._get_correct_answer().lower()

        # Check if answer is correct (case-insensitive, strip whitespace)
        is_correct = user_answer == correct_answer

        # Update SRS
        self.srs.record_answer(self.current_question_id, is_correct)

        # Show feedback
        if is_correct:
            self.feedback_text.value = "✔ Correct!"
            self.feedback_text.color = ft.Colors.GREEN_400
        else:
            self.feedback_text.value = f"✘ Not quite. The correct answer is '{self._get_correct_answer()}'."
            self.feedback_text.color = ft.Colors.RED_400

        # Show explanation if available
        if "explanation" in self.current_question:
            self.explanation_text.value = self.current_question["explanation"]

        safe_update(self.feedback_text, self.explanation_text)

        # Save SRS data
        self.page.run_task(self._save_srs_data)

        # Update statistics
        self._update_stats()

        # Auto-advance if correct
        if is_correct:
            self.page.run_task(self._auto_advance)

    async def _auto_advance(self) -> None:
        """Auto-advance to next question after a short delay."""
        await asyncio.sleep(1.2)
        self._load_next_due_question()

    def _on_skip(self, _: ft.ControlEvent) -> None:
        """Skip to the next question without recording an answer."""
        self._load_next_due_question()

    def _on_refresh_stats(self, _: ft.ControlEvent) -> None:
        """Refresh the statistics display."""
        self._update_stats()
        self._show_snack_bar("Statistics refreshed!")

    def _update_stats(self) -> None:
        """Update the statistics display."""
        stats = self.srs.get_stats()

        # Overall stats
        self.overall_stats_text.value = (
            f"📊 Total Reviews: {stats['total_reviews']}\n"
            f"✅ Correct: {stats['total_correct']}\n"
            f"❌ Incorrect: {stats['total_incorrect']}\n"
            f"🎯 Accuracy: {stats['accuracy']:.1f}%\n"
            f"🔥 Current Streak: {stats['streak']}\n"
            f"🏆 Best Streak: {stats['best_streak']}"
        )

        # Topic stats
        topic_stats = self.srs.get_topic_stats()
        self.topic_stats_container.controls.clear()

        for topic, tstats in sorted(topic_stats.items()):
            if tstats["total"] > 0:
                stat_text = ft.Text(
                    f"{topic}: {tstats['correct']}/{tstats['total']} ({tstats['accuracy']:.0f}%)",
                    size=12,
                )
                self.topic_stats_container.controls.append(stat_text)

        safe_update(self.overall_stats_text, self.topic_stats_container)

    async def _load_srs_data(self) -> None:
        """Load SRS data from client storage."""
        try:
            data_str = await self.page.client_storage.get_async("srs_data")
            if data_str:
                import json
                data = json.loads(data_str)
                self.srs.from_dict(data)
        except Exception as e:
            print(f"Error loading SRS data: {e}")

    async def _save_srs_data(self) -> None:
        """Save SRS data to client storage."""
        try:
            import json
            data = self.srs.to_dict()
            data_str = json.dumps(data)
            await self.page.client_storage.set_async("srs_data", data_str)
        except Exception as e:
            print(f"Error saving SRS data: {e}")

    def _show_snack_bar(self, message: str) -> None:
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()


def main(page: ft.Page) -> None:
    page.title = "Italian Learning Toolkit"
    page.padding = 5  # Minimal padding for narrow screens
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.CrossAxisAlignment.START
    
    # Only set window size for desktop apps (not web)
    import os
    if os.getenv("FLET_WEB_MODE", "").lower() != "true":
        try:
            page.window_width = 1200
            page.window_height = 800
        except AttributeError:
            # Window properties not available (web mode)
            pass

    theme_switch = ft.Switch(label="Dark mode", value=True)
    
    # Settings panel (visible by default for now)
    user_id_field = ft.TextField(
        label="User ID (for cross-device sync)",
        hint_text="Enter a unique ID to sync progress across devices",
        expand=True,
    )
    sync_status = ft.Text("Local mode (enter ID to sync)", size=11, color=ft.Colors.ON_SURFACE_VARIANT)

    async def save_user_id(user_id: str) -> None:
        """Save user ID and reload progress."""
        await set_user_id(page, user_id)
        user_id_field.value = user_id
        safe_update(user_id_field)
        
        # Reload progress from cloud
        page.run_task(article_view._load_progress)
        page.run_task(verb_view._load_progress)
        page.run_task(preposition_view._load_progress)
        
        sync_status.value = f"Synced as: {user_id}" if user_id else "Local mode"
        sync_status.color = ft.Colors.GREEN_400 if user_id else ft.Colors.ON_SURFACE_VARIANT
        safe_update(sync_status)
        page.snack_bar = ft.SnackBar(ft.Text(f"User ID saved! Progress will sync across devices." if user_id else "Using local storage only."))
        page.snack_bar.open = True
        page.update()

    def on_user_id_submit(e: ft.ControlEvent) -> None:
        user_id = user_id_field.value.strip()
        page.run_task(save_user_id, user_id)

    user_id_field.on_submit = lambda e: on_user_id_submit(e)
    save_user_id_btn = ft.ElevatedButton("Save ID", icon="cloud_sync", on_click=lambda _: on_user_id_submit(_))

    async def load_user_id() -> None:
        """Load saved user ID."""
        user_id = await get_user_id(page)
        user_id_field.value = user_id
        if user_id:
            sync_status.value = f"Synced as: {user_id}"
            sync_status.color = ft.Colors.GREEN_400
        else:
            sync_status.value = "Local mode (enter ID to sync)"
            sync_status.color = ft.Colors.ON_SURFACE_VARIANT
        safe_update(user_id_field, sync_status)

    page.run_task(load_user_id)

    def toggle_theme(e: ft.ControlEvent) -> None:
        page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        page.update()

    theme_switch.on_change = toggle_theme

    # Settings panel at the top
    settings_panel = ft.Container(
        content=ft.Row(
            [
                user_id_field,
                save_user_id_btn,
                sync_status,
            ],
            spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=8,
        bgcolor=CARD_BG,
        border_radius=6,
        visible=True,
    )

    page.appbar = ft.AppBar(
        title=ft.Text("Italian Learning Toolkit"),
        center_title=False,
        actions=[
            ft.Container(theme_switch, padding=ft.padding.only(right=16)),
        ],
    )

    reference_view = ReferenceView(page, ChatClient(OPENAI_API_KEY))
    article_view = ArticleExerciseView(page)
    verb_view = VerbExerciseView(page)
    preposition_view = PrepositionExerciseView(page)

    # New exercise views
    pronunciation_view = GenericExerciseView(
        page, "Pronunciation Practice", "Test your Italian pronunciation knowledge",
        PRONUNCIATION_QUESTIONS, PRONUNCIATION_OPTIONS, "pronunciation_exercise"
    )
    greeting_view = GenericExerciseView(
        page, "Greetings Practice", "Choose the right greeting for each situation",
        GREETING_QUESTIONS, GREETING_OPTIONS, "greeting_exercise"
    )
    time_view = GenericExerciseView(
        page, "Telling Time Practice", "Practice telling time in Italian",
        TIME_QUESTIONS, TIME_OPTIONS, "time_exercise"
    )
    weather_view = GenericExerciseView(
        page, "Weather Practice", "Translate weather descriptions to Italian",
        WEATHER_QUESTIONS, WEATHER_OPTIONS, "weather_exercise"
    )
    color_view = GenericExerciseView(
        page, "Color Agreement Practice", "Practice color agreement with nouns",
        COLOR_QUESTIONS, COLOR_OPTIONS, "color_exercise"
    )
    clothing_view = GenericExerciseView(
        page, "Clothing Vocabulary", "Translate clothing items to Italian",
        CLOTHING_QUESTIONS, CLOTHING_OPTIONS, "clothing_exercise"
    )
    day_month_view = GenericExerciseView(
        page, "Days & Months", "Practice days of the week and months of the year",
        DAY_MONTH_QUESTIONS, DAY_MONTH_OPTIONS, "day_month_exercise"
    )
    question_word_view = GenericExerciseView(
        page, "Question Words", "Match Italian question words to their meanings",
        QUESTION_WORD_QUESTIONS, QUESTION_WORD_OPTIONS, "question_word_exercise"
    )
    possessive_view = GenericExerciseView(
        page, "Possessive Pronouns", "Practice Italian possessive pronouns",
        POSSESSIVE_QUESTIONS, POSSESSIVE_OPTIONS, "possessive_exercise"
    )
    family_view = GenericExerciseView(
        page, "Family Vocabulary", "Learn Italian family member names",
        FAMILY_QUESTIONS, FAMILY_OPTIONS, "family_exercise"
    )
    piacere_view = GenericExerciseView(
        page, "Piacere & Mancare", "Practice 'like' and 'miss' verb forms",
        PIACERE_QUESTIONS, PIACERE_OPTIONS, "piacere_exercise"
    )
    body_view = GenericExerciseView(
        page, "Body Parts", "Learn Italian body part vocabulary",
        BODY_QUESTIONS, BODY_OPTIONS, "body_exercise"
    )

    # Combined review with spaced repetition
    combined_review_view = CombinedReviewView(page)

    # Simplified tab structure for mobile compatibility
    practice_tabs = ft.Tabs(
        tabs=[
            ft.Tab(text="Articles", content=article_view.view),
            ft.Tab(text="Verbs", content=verb_view.view),
            ft.Tab(text="Prepositions", content=preposition_view.view),
            ft.Tab(text="Pronunciation", content=pronunciation_view.view),
            ft.Tab(text="Greetings", content=greeting_view.view),
            ft.Tab(text="Time", content=time_view.view),
            ft.Tab(text="Weather", content=weather_view.view),
            ft.Tab(text="Colors", content=color_view.view),
            ft.Tab(text="Clothing", content=clothing_view.view),
            ft.Tab(text="Days & Months", content=day_month_view.view),
            ft.Tab(text="Question Words", content=question_word_view.view),
            ft.Tab(text="Possessive", content=possessive_view.view),
            ft.Tab(text="Family", content=family_view.view),
            ft.Tab(text="Piacere/Mancare", content=piacere_view.view),
            ft.Tab(text="Body Parts", content=body_view.view),
        ],
        scrollable=True,
        expand=True,
    )

    main_tabs = ft.Tabs(
        tabs=[
            ft.Tab(text="Reference", content=reference_view.view),
            ft.Tab(text="Practice", content=practice_tabs),
            ft.Tab(text="Combined Review", content=combined_review_view.view),
        ],
        scrollable=True,
        expand=True,
    )

    # Main content area
    main_content = ft.Column(
        [
            settings_panel,
            main_tabs,
        ],
        spacing=8,
        expand=True,
    )
    
    page.add(main_content)
    reference_view.prime()
    page.update()


if __name__ == "__main__":
    # Run in web mode for cloud deployment
    # Use: ft.app(target=main, view=ft.AppView.WEB_BROWSER) for web-only
    # Or: ft.app(target=main) for desktop with web option
    import os
    if os.getenv("FLET_WEB_MODE", "").lower() == "true":
        ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=int(os.getenv("PORT", "8550")))
    else:
        ft.app(target=main)

