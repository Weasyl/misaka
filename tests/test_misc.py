# -*- coding: utf-8 -*-

from chibitest import TestCase, ok
from misaka import (
    HtmlRenderer,
    Markdown,
    extension_map,
    EXT_TABLES,
    EXT_FENCED_CODE,
    EXT_FOOTNOTES,
    EXT_NO_INTRA_EMPHASIS,
)
from misaka.utils import args_to_int


class ArgsToIntTest(TestCase):
    def test_args(self):
        expected = EXT_TABLES | EXT_FENCED_CODE | EXT_FOOTNOTES
        result = args_to_int(
            extension_map,
            ('tables', 'fenced-code', 'footnotes'))

        ok(result) == expected

    def test_int(self):
        expected = EXT_TABLES | EXT_FENCED_CODE | EXT_FOOTNOTES
        result = args_to_int(extension_map, expected)

        ok(result) == expected


class MarkdownParserTest(TestCase):
    def setup(self):
        self.r = Markdown(HtmlRenderer())

    def render_with(self, text, extensions=0):
        return Markdown(HtmlRenderer(), extensions)(text)

    def test_nested_bold_italics(self):
        markdown = self.r('*foo **bar** baz*')
        ok(markdown).diff('<p><em>foo <strong>bar</strong> baz</em></p>\n')

        markdown = self.r(r'*foo\**')
        ok(markdown).diff('<p><em>foo*</em></p>\n')

    def test_punctuation_before_emphasis(self):
        markdown = self.render_with('%*test*', extensions=EXT_NO_INTRA_EMPHASIS)
        ok(markdown).diff('<p>%<em>test</em></p>\n')

        markdown = self.render_with('~**test**', extensions=EXT_NO_INTRA_EMPHASIS)
        ok(markdown).diff('<p>~<strong>test</strong></p>\n')

    def test_list_custom_start(self):
        class ListCustomStartRenderer(HtmlRenderer):
            def list(self, text, is_ordered, is_block, prefix):
                if prefix:
                    return '<ol start="{start}">\n{text}</ol>\n'.format(
                        start=prefix,
                        text=text)

                return super(ListCustomStartRenderer, self).list(text, is_ordered, is_block, prefix)

        text = ' 5. five\n 6. six\n 7. seven'
        rendered = Markdown(ListCustomStartRenderer())(text)
        ok(rendered).diff('<ol start="5">\n<li>five</li>\n<li>six</li>\n<li>seven</li>\n</ol>\n')
