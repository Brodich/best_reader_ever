from dataclasses import dataclass
from configparser import ConfigParser
import logging
@dataclass
class text_processor:
    filename: str = 'config.ini'
    
    def __post_init__(self) -> None:
        """Initialize text_processor client and configure logging."""
        self._setup_config()
        self._setup_logging()
        self.logger.info("text_processor initialized")

    def _setup_config(self) -> None:
        """Read configuration from INI file."""
        self.cfg = ConfigParser()
        self.cfg.read(self.filename)
        
        self.lines = int(self.cfg.get('text_processor', 'lines'))
        self.chars = int(self.cfg.get('text_processor', 'chars'))
        self.log_file = self.cfg.get('text_processor', 'log_file')

    def _setup_logging(self) -> None:
        """Configure logging system."""
        self.logger  = logging.getLogger(self.log_file)
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(self.log_file, mode='a')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        self.logger.addHandler(file_handler)

    def chapt_process(self, chapters:list):
        ans = [[]]
        cur_l = 0
        for i in chapters:
            l = len(i)//self.chars + (len(i)%self.chars>0)
            if l+cur_l <= self.lines or len(ans[-1])==0:
                cur_l+=l
                ans[-1].append(i)
            else:
                cur_l = l
                ans.append([i])
        return ans

    def process(self, text: str) -> None:
        if not text:
            self.logger.error('Empty text')
            return False
        chapters = text.split('\n') if '\n' in text else [text]
        pages = self.chapt_process(chapters)
        return pages