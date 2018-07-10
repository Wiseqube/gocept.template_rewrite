import pytest
from gocept.template_rewrite.pagetemplates import PTParserRewriter
from gocept.template_rewrite.lib2to3 import rewite_using_2to3


@pytest.mark.parametrize('input, expected', [
    ('<p tal:define="x d; y python: str(234); z python: 5; a d"></p>',
     '<p tal:define="x d; y python:rewritten; z python:rewritten; a d"></p>'),
    ('<tal:t define="x d; y python: str(234); z python: 5; a d"></tal:t>',
     '<tal:t define="x d; y python:rewritten; z python:rewritten; a d">'
     '</tal:t>'),
])
def test_pagetemplates__PTParserRewriter____call____1(
        input, expected):
    """It rewrites the expression values of the pagetemplate."""
    rw = PTParserRewriter(input, lambda x: "rewritten")
    assert rw() == expected


@pytest.mark.parametrize('input, expected', [
    ('<p tal:content="python: str(234)" class="python:script"></p>',
     '<p tal:content="python:rewritten" class="python:script"></p>'),
    ('''<p tal:define="x d; y python: str(';;'); z python: 5"></p>''',
     '<p tal:define="x d; y python:rewritten; z python:rewritten"></p>'),
    ('<tal:t content="python: str(234)" class="python:script"></tal:t>',
     '<tal:t content="python:rewritten" class="python:rewritten"></tal:t>'),
    ('''<tal:t define="x d; y python: str(';;'); z python: 5"></tal:t>''',
     '<tal:t define="x d; y python:rewritten; z python:rewritten"></tal:t>'),
])
def test_pagetemplates__PTParserRewriter____call____1_2(
        input, expected):
    """It rewrites the expression values of the pagetemplate.

    (working well with PTParserRewriter)
    """
    rw = PTParserRewriter(input, lambda x: "rewritten")
    assert rw() == expected


@pytest.mark.parametrize('input, expected', [
    ('''<p tal:define="y python: str(';;')"></p>''',
     '''<p tal:define="y python: unicode(';;')"></p>'''),
    ('''<tal:t define="y python: str(';;')"></tal:t>''',
     '''<tal:t define="y python: unicode(';;')"></tal:t>'''),
    ('''<p tal:define="y python: str(';;;;')"></p>''',
     '''<p tal:define="y python: unicode(';;;;')"></p>'''),
    ('''<tal:t define="y python: str(';;;;')"></tal:t>''',
     '''<tal:t define="y python: unicode(';;;;')"></tal:t>'''),
])
def test_pagetemplates__PTParserRewriter____call____2(
        input, expected):
    """It can work with double semicolon (escape for a single one)."""
    rw = PTParserRewriter(input, lambda x: x.replace('str', 'unicode'))
    assert rw() == expected


@pytest.mark.parametrize('input', [
    ('''
<button tal:attributes="onclick string:go('view?id=${item/is}&re_url=redir')">
        </button>'''),
    ('''
<tal:x condition="item/desc"
       replace="structure python:item.replace('\n','<br/>')"/>'''),
    # We have the name of an attribute occuring after it in the tag.
    ('''
<input type="hidden"
       id="selector"
       name="id"
       tal:attributes="value request/id|nothing">'''),
    ('''
<input type="hidden"
       id="selector"
       name="id"
       disabled
       tal:attributes="disabled view/disabled">'''),
    ('<!-- Support for an on-screen keyboard -->'),
    ('''
<!-- Support for an
        on-screen keyboard -->'''),
    ('''
<p>Documents with multiple document root tags</p>
<p>are not valid XML.</p>
'''),
    ('''
<p>Can we parse entities</p>
&nbsp;
<p>between tags</p>
'''),
    ('''<p>Can we parse character references &#x34;</p> '''),
    # Processing instruction
    '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>''',
    # It does not change string expressions
    '''<a tal:content="string:${view/b};;3">a</a>''',
    # It keeps the escapable characters in script tags.
    '''<script> a <> 2 & 4 </script>''',
    # But also keeps entity references.
    '''<p> a &lt;&gt; 2 &amp; 4</p>''',
    # Weird casing of attributes
    '''<a href="#" onClick="window.open('ttwidget_html')">New window</a>''',
    '''<a href="#" disAbled>New window</a>''',
    # Broken HTML without TAL statements
    '''<count y;not any nw in x$y;1b];0b]}\n\nread:>''',
])
def test_pagetemplates__PTParserRewriter____call____3(
        input):
    """It can handle some edge cases in pagetemplates."""
    rw = PTParserRewriter(input, lambda x: x)
    assert rw() == input


@pytest.mark.parametrize('input, expected', [
    ('<p tal:content="python: long(a)"></p>',
     '<p tal:content="python:int(a)"></p>',),
])
def test_pagetemplates__PTParserRewriter____call____4(
        input, expected):
    """It can be used with a preconfigured 2to3 rewrite_action."""
    rw = PTParserRewriter(input, rewite_using_2to3)
    assert rw() == expected
