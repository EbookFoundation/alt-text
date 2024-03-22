from abc import ABC, abstractmethod


class LangEngine(ABC):
    @abstractmethod
    def _completion(self, prompt: str) -> str:
        """Sends message to language model and returns its response.

        Args:
            prompt (str): Prompt to send to language model.

        Returns:
            str: Response from language model.
        """
        pass

    @abstractmethod
    def refineDesc(self, description: str) -> str:
        """Refines description of an image.
        Used in V1 Dataflow.

        Args:
            description (str): Description of an image.

        Returns:
            str: Refinement of description.
        """
        pass

    @abstractmethod
    def refineOCR(self, chars: str) -> str:
        """Refines characters found in an image.
        Used in V1 Dataflow.

        Args:
            chars (str): Characters found in an image.

        Returns:
            str: Refinement of characters.
        """
        pass

    @abstractmethod
    def genPrompt(self, desc: str, chars: str, context: list[str], caption: str) -> str:
        """Generates prompt to send to language model in V2 Dataflow.

        Args:
            desc (str): Description of an image.
            chars (str): Characters found in an image.
            context (list[str]): Context of an image. See getContext in alttext for more information.
            caption (str): Caption of an image.

        Returns:
            str: Prompt to send to language model.
        """
        pass

    @abstractmethod
    def refineAlt(
        self,
        desc: str,
        chars: str = None,
        context: list[str] = None,
        caption: str = None,
    ) -> str:
        """Generates alt-text for an image.
        Used in V2 Dataflow.

        Args:
            desc (str): Description of an image.
            chars (str, optional): Characters found in an image. Defaults to None.
            context (list[str], optional): Context of an image. See getContext in alttext for more information. Defaults to None.
            caption (str, optional): Caption of an image. Defaults to None.

        Returns:
            str: Alt-text for an image.
        """
        pass

    @abstractmethod
    def ingest(self, filename: str, binary) -> bool:
        """Ingests a file into the language model.

        Args:
            filename (str): Name of file.
            binary (_type_): Data of file.

        Returns:
            bool: True if successful.
        """
        pass

    @abstractmethod
    def degest(self, filename: str) -> bool:
        """Removes a file from the language model.

        Args:
            filename (str): Name of file.

        Returns:
            bool: True if successful.
        """
        pass
