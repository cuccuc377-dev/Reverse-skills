from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import docking.widgets.fieldpanel.support
import ghidra.app.nav
import ghidra.app.util.viewer.listingpanel
import ghidra.debug.api.action
import java.lang # type: ignore


class DebuggerListing(ghidra.app.nav.Navigatable):

    class_: typing.ClassVar[java.lang.Class]

    def getTitle(self) -> str:
        """
        Get the window title of this debugger listing
        
        :return: Title of window
        :rtype: str
        """

    def isMainListing(self) -> bool:
        """
        Returns boolean if this listing is the main debugger listing
        
        :return: true/false if this is the main listing
        :rtype: bool
        """

    def setCustomTitle(self, title: typing.Union[java.lang.String, str]) -> None:
        """
        Set a custom title.
         
        
        Setting the title here prevents future calls to
        :meth:`docking.ComponentProvider.setTitle(String) <docking.ComponentProvider.setTitle>` from having any effect. This is done to
        preserve the custom
        title.
        
        :param java.lang.String or str title: the title
        """

    def setFollowsCurrentThread(self, follows: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Set if this debugger listing should follow the current thread when displaying
        
        :param jpype.JBoolean or bool follows: true/false if this listing should follow the current thread
        """

    def setTrackingSpec(self, spec: ghidra.debug.api.action.LocationTrackingSpec) -> None:
        """
        Set what this debugger listing should track as the user performs actions
        
        :param ghidra.debug.api.action.LocationTrackingSpec spec: :obj:`LocationTrackingSpec` describing how/what the listing will track
        """

    @property
    def mainListing(self) -> jpype.JBoolean:
        ...

    @property
    def title(self) -> java.lang.String:
        ...


class MultiBlendedListingBackgroundColorModel(ghidra.app.util.viewer.listingpanel.ListingBackgroundColorModel):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self) -> None:
        ...

    def addModel(self, m: docking.widgets.fieldpanel.support.BackgroundColorModel) -> None:
        ...

    def removeModel(self, m: docking.widgets.fieldpanel.support.BackgroundColorModel) -> None:
        ...



__all__ = ["DebuggerListing", "MultiBlendedListingBackgroundColorModel"]
