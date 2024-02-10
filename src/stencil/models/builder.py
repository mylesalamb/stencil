"""
stencil builtin builders,

objects that are responsible for recieving input files and 'building' them
to outputs with some particular strategy
"""
import pathlib
import shutil
from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional
from typing import Type

import markdown
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template
from stencil.models.content import Artefact
from stencil.models.context import BuildContext
from stencil.util.config import StencilBuilder
from stencil.util.exceptions import StencilException
from stencil.util.metadata import get_file_content


class Builder(ABC):
    """
    Abstract class that represents some method of building inputs to outputs
    """

    def __init__(self, name: str) -> None:
        self._name = name
        self._content: List[Artefact] = []

    @abstractmethod
    def build(self, ctx: BuildContext) -> None:
        """
        Given the content stored inside the builder, process the content to build outputs
        """

    def add_content(self, ctx: BuildContext, content: Artefact) -> None:
        """
        Registers content to the builder
        """
        del ctx
        self._content.append(content)

    def __repr__(self) -> str:
        attrs = ", ".join([f"{key}={value}" for key, value in vars(self).items()])
        return f"{self.__class__.__name__}({attrs})"


class MarkdownBuilder(Builder):
    """
    Build strategy that takes markdown documents as an input
    """

    def __init__(
        self,
        name: str,
        template_directory: pathlib.Path,
        markdown_extensions: Optional[list[str]] = None,
        recursive: bool = False,
    ) -> None:
        super().__init__(name)
        self._template_env = Environment(loader=FileSystemLoader([template_directory]))
        self._recursive = recursive
        self._markdown_extensions = markdown_extensions or []

    def _build_artefact(self, ctx: BuildContext, artefact: Artefact) -> str:
        metadata, content = get_file_content(artefact.source)

        template_name = metadata.get("template")
        if not template_name:
            raise StencilException("No template provided")

        body = markdown.markdown(content, extensions=self._markdown_extensions)

        template = self._template_env.get_template(template_name)
        current = template.render(content=body, metadata=metadata, ctx=ctx)
        previous = None

        if not self._recursive:
            return current

        while current != previous:
            previous = current
            current = Template(current).render(metadata=metadata, ctx=ctx)

        return current

    def add_content(self, ctx: BuildContext, content: Artefact) -> None:
        """
        Registers content to the builder
        """
        super().add_content(ctx, content)
        metadata, _ = get_file_content(content.source)
        name = metadata.get("name") or content.source.name
        ctx.register_content(name, content, metadata)

    def build(self, ctx: BuildContext) -> None:
        for artefact in self._content:
            destination = ctx.output_directory / artefact.destination
            destination.parent.mkdir(exist_ok=True, parents=True)
            content = self._build_artefact(ctx, artefact)
            with open(destination, "w", encoding="utf-8") as f:
                f.write(content)


class HTMLBuilder(Builder):
    """
    Build strategy for building templated HTML with jinja2
    """

    def __init__(
        self, name: str, template_directory: pathlib.Path, recursive: bool = False
    ) -> None:
        super().__init__(name)
        self._template_env = Environment(loader=FileSystemLoader([template_directory]))
        self._recursive = recursive

    def _build_artefact(self, ctx: BuildContext, artefact: Artefact) -> str:
        metadata, body = get_file_content(artefact.source)

        template_name = metadata.get("template")
        if not template_name:
            raise StencilException("No template provided")

        template = self._template_env.get_template(template_name)
        current = template.render(content=body, metadata=metadata, ctx=ctx)
        if not self._recursive:
            return current

        previous = None
        while current != previous:
            previous = current
            current = Template(current).render(ctx=ctx, metadata=metadata)

        return current

    def add_content(self, ctx: BuildContext, content: Artefact) -> None:
        """
        Registers content to the builder
        """
        super().add_content(ctx, content)
        metadata, _ = get_file_content(content.source)
        name = metadata.get("name") or content.source.name
        ctx.register_content(name, content, metadata)

    def build(self, ctx: BuildContext) -> None:
        for artefact in self._content:
            destination = ctx.output_directory / artefact.destination
            content = self._build_artefact(ctx, artefact)
            with open(destination, "w", encoding="utf-8") as f:
                f.write(content)


class StaticBuilder(Builder):
    """
    Build strategy that takes markdown documents as an input
    """

    def __init__(self, name: str, symlink: bool = False) -> None:
        super().__init__(name)
        self._symlink: bool = symlink

    def build(self, ctx: BuildContext) -> None:
        for artefact in self._content:
            destination = ctx.output_directory / artefact.destination
            destination.parent.mkdir(exist_ok=True, parents=True)
            shutil.copy(artefact.source, destination)

    def add_content(self, ctx: BuildContext, content: Artefact) -> None:
        """
        Registers content to the builder
        """
        super().add_content(ctx, content)
        ctx.register_content(content.source.name, content)


def construct(name: str, builder: StencilBuilder) -> Builder:
    """
    Given the name of some builder type and the kwargs for its consructor

    return an instantiation of the type
    """

    # Needs type annotation https://github.com/python/mypy/issues/1843
    builders: List[Type[Builder]] = Builder.__subclasses__()
    builder_type = next(
        (elt for elt in builders if elt.__name__ == builder.flavor), None
    )
    if not builder_type:
        raise StencilException(f"No builder for flavor {builder_type}")

    return builder_type(name=name, **builder.config)
