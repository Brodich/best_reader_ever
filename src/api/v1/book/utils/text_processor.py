from dataclasses import dataclass

from src.utils.settings import settings


@dataclass
class TextProcessor:
    def __post_init__(self) -> None:
        self._setup_config()

    def _setup_config(self) -> None:
        self.lines = settings.PAGE_LINES
        self.chars = settings.PAGE_CHARS

    def chapt_process(self, chapters: list):
        result = [[]]
        cur_l = 0
        for chapter in chapters:
            l = len(chapter) // self.chars + (len(chapter) % self.chars > 0)
            if l + cur_l <= self.lines or len(result[-1]) == 0:
                cur_l += l
                result[-1].append(chapter)
            else:
                cur_l = l
                result.append([chapter])
        return result

    def process(self, text: str) -> None:
        if not text:
            return
        chapters = text.split("\n") if "\n" in text else [text]
        pages = self.chapt_process(chapters)
        return pages
