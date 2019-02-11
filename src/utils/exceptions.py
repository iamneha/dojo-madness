#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Representation of HTTP error."""
from werkzeug.exceptions import HTTPException


class HTTPError(HTTPException):
    """Representation of HTTP error."""

    def __init__(self, status_code, error=None):
        """Call the superclass constructor and set status code and error attributes."""
        super().__init__(self)
        self.code = status_code
        self.description = error or self._get_description_by_code(status_code) or ''
        self.data = {'error': self.description}

    @staticmethod
    def _get_description_by_code(status_code):
        _code_desc = {}
        for child in HTTPException.__subclasses__():
            _code = getattr(child, 'code')
            _desc = getattr(child, 'description')
            if _code and _desc:
                _code_desc[_code] = _desc
        return _code_desc.get(status_code)
