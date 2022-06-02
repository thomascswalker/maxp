from __future__ import annotations

from typing import Callable, List, Union

from maxp import scene, rt

global HANDLERS
HANDLERS: List[When] = []
if not isinstance(HANDLERS, list):
    HANDLERS = []


class Manager:
    handlers: List[When] = []


class Attribute:
    """These specify the attribute of the given object(s) to be tracked for change."""

    Topology: str = "topology"
    """Signaled when the topology of an object changes in
    the Modify panel such as, using a mesh smooth, optimize, or vertex delete."""
    Geometry: str = "geometry"
    """Signaled when the geometry of an object changes such as, by moving a vertex
    or using an animated modifier."""
    Names: str = "names"
    """Signaled when the name of an object is changed if this occurs because a user
    edits the name in one of the 3ds Max command panels. The handler is called
    repeatedly with each character that is changed."""
    Transform: str = "transform"
    """Signaled when the transform of an object is changed such as, by a move, rotate,
    or scale."""
    Select: str = "select"
    """Signaled when a scene node moves into or out of the current selection set. You
    should interrogate the <node>.isSelected property to determine the new state."""
    Parameters: str = "parameters"
    """Signaled when any parameters are changed in the object. This is something of a
    catch all because the core signals this event in many situations."""
    SubAnimStructure: str = "subAnimStructure"
    """Signaled when the dynamic subAnim structure changes such as, when a new vertex
    becomes animated in an editable mesh, or when a new controller is added to a list
    controller. Also called when subAnims are reassigned, for example, when a material
    is changed in an object."""
    Controller: str = "controller"
    """Signaled when a new controller is assigned to one of the object's tracks."""
    Children: str = "children"
    """Signaled when an object has immediate children added or removed."""


class Trigger:
    """These specify the type of triggered event."""

    Changes: str = "changes"
    """Execute on the change of an Attribute."""
    Deleted: str = "deleted"
    """Execute on the deletion of the node."""


class HandleMode:
    """These specify when to handle the event."""

    RedrawViews: rt.Name = rt.Name("redrawViews")
    """Execute when the viewport redraws views."""
    TimeChange: rt.Name = rt.Name("timeChange")
    """Execute when the animation time is changed."""


class When:
    """Wrapper for the when construct in MAXScript.

    The when construct defines a change handler function for a certain type of event on
    one or more objects. The system then automatically calls this function whenever
    the event occurs.
    """

    def __init__(
        self,
        objs: Union[rt.Node, List[rt.Node]],
        trigger: Trigger,
        method: Callable,
        attr: Attribute = None,
        handleAt: HandleMode = HandleMode.RedrawViews,
    ) -> None:
        objs = [objs] if not isinstance(objs, list) else objs
        for obj in objs:
            if scene.isValid(obj):
                continue
            raise ValueError(f"{obj} is invalid.")
        self._objs = objs
        self._trigger = trigger
        if not callable(method):
            raise ValueError(f"{method} method is not callable.")
        self._method = method
        self._attr = attr
        self._handleAt = handleAt
        self._exec()

    def _exec(self) -> None:
        if self._trigger == Trigger.Changes and self._attr is None:
            raise ValueError(
                "The change trigger requires an Attribute to be set."
                "Use the attr= parameter"
            )
        rt._tempMethod = self._method
        mxsArray = "#(" + ",".join(["$" + obj.name for obj in self._objs]) + ")"
        mxs = (
            f"when {self._attr} {mxsArray} {self._trigger} "
            f"handleAt:#{self._handleAt} node do ("
            "_tempMethod node"
            ")"
        )
        handler = rt.Execute(mxs)
        HANDLERS.append(handler)


class GeneralEvent:
    unitsChange: str = "unitsChange"
    timeunitsChange: str = "timeunitsChange"
    viewportChange: str = "viewportChange"
    spacemodeChange: str = "spacemodeChange"
    systemPreReset: str = "systemPreReset"
    systemPostReset: str = "systemPostReset"
    systemPreNew: str = "systemPreNew"
    systemPostNew: str = "systemPostNew"
    filePreOpen: str = "filePreOpen"
    filePostOpen: str = "filePostOpen"
    filePreMerge: str = "filePreMerge"
    filePostMerge: str = "filePostMerge"
    filePreSave: str = "filePreSave"
    filePostSave: str = "filePostSave"
    fileOpenFailed: str = "fileOpenFailed"
    filePreSaveOld: str = "filePreSaveOld"
    filePostSaveOld: str = "filePostSaveOld"
    selectionSetChanged: str = "selectionSetChanged"
    bitmapChanged: str = "bitmapChanged"
    preRender: str = "preRender"
    postRender: str = "postRender"
    preRenderframe: str = "preRenderframe"
    postRenderframe: str = "postRenderframe"
    preImport: str = "preImport"
    postImport: str = "postImport"
    importFailed: str = "importFailed"
    preExport: str = "preExport"
    postExport: str = "postExport"
    exportFailed: str = "exportFailed"
    preProgress: str = "preProgress"
    postProgress: str = "postProgress"
    modpanelSelChanged: str = "modpanelSelChanged"
    rendparamChanged: str = "rendparamChanged"
    matlibPreOpen: str = "matlibPreOpen"
    matlibPostOpen: str = "matlibPostOpen"
    matlibPreSave: str = "matlibPreSave"
    matlibPostSave: str = "matlibPostSave"
    matlibPreMerge: str = "matlibPreMerge"
    matlibPostMerge: str = "matlibPostMerge"
    filelinkBindFailed: str = "filelinkBindFailed"
    filelinkDetachFailed: str = "filelinkDetachFailed"
    filelinkReloadFailed: str = "filelinkReloadFailed"
    filelinkAttachFailed: str = "filelinkAttachFailed"
    filelinkPreBind: str = "filelinkPreBind"
    filelinkPostBind: str = "filelinkPostBind"
    filelinkPreDetach: str = "filelinkPreDetach"
    filelinkPostDetach: str = "filelinkPostDetach"
    filelinkPreReload: str = "filelinkPreReload"
    filelinkPostReload: str = "filelinkPostReload"
    filelinkPreAttach: str = "filelinkPreAttach"
    filelinkPostAttach: str = "filelinkPostAttach"
    renderPreeval: str = "renderPreeval"
    nodeCreated: str = "nodeCreated"
    nodeLinked: str = "nodeLinked"
    nodeUnlinked: str = "nodeUnlinked"
    nodeHide: str = "nodeHide"
    nodeUnhide: str = "nodeUnhide"
    nodeFreeze: str = "nodeFreeze"
    nodeUnfreeze: str = "nodeUnfreeze"
    nodePreMtl: str = "nodePreMtl"
    nodePostMtl: str = "nodePostMtl"
    sceneAddedNode: str = "sceneAddedNode"
    scenePreDeletedNode: str = "scenePreDeletedNode"
    scenePostDeletedNode: str = "scenePostDeletedNode"
    selNodesPreDelete: str = "selNodesPreDelete"
    selNodesPostDelete: str = "selNodesPostDelete"
    wmEnable: str = "wmEnable"
    systemShutdown: str = "systemShutdown"
    systemStartup: str = "systemStartup"
    pluginLoaded: str = "pluginLoaded"
    systemShutdown2: str = "systemShutdown2"
    animateOn: str = "animateOn"
    animateOff: str = "animateOff"
    colorChange: str = "colorChange"
    preEditObjChange: str = "preEditObjChange"
    postEditObjChange: str = "postEditObjChange"
    radiosityprocessStarted: str = "radiosityprocessStarted"
    radiosityprocessStopped: str = "radiosityprocessStopped"
    radiosityprocessReset: str = "radiosityprocessReset"
    radiosityprocessDone: str = "radiosityprocessDone"
    lightingUnitDisplaySystemChange: str = "lightingUnitDisplaySystemChange"
    beginRenderingReflectRefractMap: str = "beginRenderingReflectRefractMap"
    beginRenderingActualFrame: str = "beginRenderingActualFrame"
    beginRenderingTonemappingImage: str = "beginRenderingTonemappingImage"
    radiosityPluginChanged: str = "radiosityPluginChanged"
    sceneUndo: str = "sceneUndo"
    sceneRedo: str = "sceneRedo"
    manipulateModeOff: str = "manipulateModeOff"
    manipulateModeOn: str = "manipulateModeOn"
    sceneXrefPreMerge: str = "sceneXrefPreMerge"
    sceneXrefPostMerge: str = "sceneXrefPostMerge"
    objectXrefPreMerge: str = "objectXrefPreMerge"
    objectXrefPostMerge: str = "objectXrefPostMerge"
    preMirrorNodes: str = "preMirrorNodes"
    postMirrorNodes: str = "postMirrorNodes"
    nodeCloned: str = "nodeCloned"
    preNotifydependents: str = "preNotifydependents"
    postNotifydependents: str = "postNotifydependents"
    mtlRefadded: str = "mtlRefadded"
    mtlRefdeleted: str = "mtlRefdeleted"
    timerangeChange: str = "timerangeChange"
    preModifierAdded: str = "preModifierAdded"
    postModifierAdded: str = "postModifierAdded"
    preModifierDeleted: str = "preModifierDeleted"
    postModifierDeleted: str = "postModifierDeleted"
    filelinkPostReloadPrePrune: str = "filelinkPostReloadPrePrune"
    preNodesCloned: str = "preNodesCloned"
    postNodesCloned: str = "postNodesCloned"
    systemPreDirChange: str = "systemPreDirChange"
    systemPostDirChange: str = "systemPostDirChange"
    svselectionSetChanged: str = "svselectionSetChanged"
    svDoubleclickGraphnode: str = "svDoubleclickGraphnode"
    preRendererChange: str = "preRendererChange"
    postRendererChange: str = "postRendererChange"
    svPreLayoutChange: str = "svPreLayoutChange"
    svPostLayoutChange: str = "svPostLayoutChange"
    byCategoryDisplayFilterChanged: str = "byCategoryDisplayFilterChanged"
    customDisplayFilterChanged: str = "customDisplayFilterChanged"
    layerCreated: str = "layerCreated"
    layerDeleted: str = "layerDeleted"
    nodeLayerChanged: str = "nodeLayerChanged"
    tabbedDialogCreated: str = "tabbedDialogCreated"
    tabbedDialogDeleted: str = "tabbedDialogDeleted"
    nodeNameSet: str = "nodeNameSet"
    hwTextureChanged: str = "hwTextureChanged"
    mxsStartup: str = "mxsStartup"
    mxsPostStartup: str = "mxsPostStartup"
    actionItemHotkeyPreExec: str = "actionItemHotkeyPreExec"
    actionItemHotkeyPostExec: str = "actionItemHotkeyPostExec"
    scenestatePreSave: str = "scenestatePreSave"
    scenestatePostSave: str = "scenestatePostSave"
    scenestatePreRestore: str = "scenestatePreRestore"
    scenestatePostRestore: str = "scenestatePostRestore"
    scenestateDelete: str = "scenestateDelete"
    scenePreUndo: str = "scenePreUndo"
    scenePreRedo: str = "scenePreRedo"
    scenePostUndo: str = "scenePostUndo"
    scenePostRedo: str = "scenePostRedo"
    mxsShutdown: str = "mxsShutdown"
    d3dPreDeviceReset: str = "d3dPreDeviceReset"
    d3dPostDeviceReset: str = "d3dPostDeviceReset"
    toolpaletteMtlSuspend: str = "toolpaletteMtlSuspend"
    toolpaletteMtlResume: str = "toolpaletteMtlResume"
    classdescReplaced: str = "classdescReplaced"
    filePreOpenProcess: str = "filePreOpenProcess"
    filePostOpenProcess: str = "filePostOpenProcess"
    filePreSaveProcess: str = "filePreSaveProcess"
    filePostSaveProcess: str = "filePostSaveProcess"
    classdescLoaded: str = "classdescLoaded"
    toolbarsPreLoad: str = "toolbarsPreLoad"
    toolbarsPostLoad: str = "toolbarsPostLoad"
    atsPreRepathPhase: str = "atsPreRepathPhase"
    atsPostRepathPhase: str = "atsPostRepathPhase"
    proxyTemporaryDisableStart: str = "proxyTemporaryDisableStart"
    proxyTemporaryDisableEnd: str = "proxyTemporaryDisableEnd"
    fileCheckStatus: str = "fileCheckStatus"
    namedSelSetCreated: str = "namedSelSetCreated"
    namedSelSetDeleted: str = "namedSelSetDeleted"
    namedSelSetPreModify: str = "namedSelSetPreModify"
    namedSelSetPostModify: str = "namedSelSetPostModify"
    modpanelSubobjectlevelChanged: str = "modpanelSubobjectlevelChanged"
    failedDirectxMaterialTextureLoad: str = "failedDirectxMaterialTextureLoad"
    renderPreevalFrameinfo: str = "renderPreevalFrameinfo"
    postSceneReset: str = "postSceneReset"
    animLayersEnabled: str = "animLayersEnabled"
    animLayersDisabled: str = "animLayersDisabled"
    actionItemPreStartOverride: str = "actionItemPreStartOverride"
    actionItemPostStartOverride: str = "actionItemPostStartOverride"
    actionItemPreEndOverride: str = "actionItemPreEndOverride"
    actionItemPostEndOverride: str = "actionItemPostEndOverride"
    preNodeGeneralPropChanged: str = "preNodeGeneralPropChanged"
    postNodeGeneralPropChanged: str = "postNodeGeneralPropChanged"
    preNodeGiPropChanged: str = "preNodeGiPropChanged"
    postNodeGiPropChanged: str = "postNodeGiPropChanged"
    preNodeMentalrayPropChanged: str = "preNodeMentalrayPropChanged"
    postNodeMentalrayPropChanged: str = "postNodeMentalrayPropChanged"
    preNodeBonePropChanged: str = "preNodeBonePropChanged"
    postNodeBonePropChanged: str = "postNodeBonePropChanged"
    preNodeUserPropChanged: str = "preNodeUserPropChanged"
    postNodeUserPropChanged: str = "postNodeUserPropChanged"
    preNodeRenderPropChanged: str = "preNodeRenderPropChanged"
    postNodeRenderPropChanged: str = "postNodeRenderPropChanged"
    preNodeDisplayPropChanged: str = "preNodeDisplayPropChanged"
    postNodeDisplayPropChanged: str = "postNodeDisplayPropChanged"
    preNodeBasicPropChanged: str = "preNodeBasicPropChanged"
    postNodeBasicPropChanged: str = "postNodeBasicPropChanged"
    selectionLock: str = "selectionLock"
    selectionUnlock: str = "selectionUnlock"
    preImageViewerDisplay: str = "preImageViewerDisplay"
    postImageViewerDisplay: str = "postImageViewerDisplay"
    imageViewerUpdate: str = "imageViewerUpdate"
    customAttributesAdded: str = "customAttributesAdded"
    customAttributesRemoved: str = "customAttributesRemoved"
    osThemeChanged: str = "osThemeChanged"
    activeViewportChanged: str = "activeViewportChanged"
    preMaxmainwindowShow: str = "preMaxmainwindowShow"
    postMaxmainwindowShow: str = "postMaxmainwindowShow"
    classdescAdded: str = "classdescAdded"
    objectDefinitionChangeBegin: str = "objectDefinitionChangeBegin"
    objectDefinitionChangeEnd: str = "objectDefinitionChangeEnd"
    mtlbaseParamdlgPreOpen: str = "mtlbaseParamdlgPreOpen"
    mtlbaseParamdlgPostClose: str = "mtlbaseParamdlgPostClose"
    preAppFrameThemeChanged: str = "preAppFrameThemeChanged"
    appFrameThemeChanged: str = "appFrameThemeChanged"
    preViewportDelete: str = "preViewportDelete"
    preWorkspaceChange: str = "preWorkspaceChange"
    postWorkspaceChange: str = "postWorkspaceChange"
    preWorkspaceCollectionChange: str = "preWorkspaceCollectionChange"
    postWorkspaceCollectionChange: str = "postWorkspaceCollectionChange"
    keyboardSettingChanged: str = "keyboardSettingChanged"
    mouseSettingChanged: str = "mouseSettingChanged"
    toolbarsPreSave: str = "toolbarsPreSave"
    toolbarsPostSave: str = "toolbarsPostSave"
    appActivated: str = "appActivated"
    appDeactivated: str = "appDeactivated"
    cuiMenusUpdated: str = "cuiMenusUpdated"
    cuiMenusPreSave: str = "cuiMenusPreSave"
    cuiMenusPostSave: str = "cuiMenusPostSave"
    viewportSafeframeToggle: str = "viewportSafeframeToggle"
    pluginsPreShutdown: str = "pluginsPreShutdown"
    pluginsPreUnload: str = "pluginsPreUnload"
    cuiMenusPostLoad: str = "cuiMenusPostLoad"
    layerParentChanged: str = "layerParentChanged"
    actionItemExecutionStarted: str = "actionItemExecutionStarted"
    actionItemExecutionEnded: str = "actionItemExecutionEnded"
    interactivePluginInstanceCreationStarted: str = (
        "interactivePluginInstanceCreationStarted"
    )
    interactivePluginInstanceCreationEnded: str = (
        "interactivePluginInstanceCreationEnded"
    )
    filePostMerge2: str = "filePostMerge2"
    postNodeSelectOperation: str = "postNodeSelectOperation"
    preViewportTooltip: str = "preViewportTooltip"
    welcomescreenDone: str = "welcomescreenDone"
    playbackStart: str = "playbackStart"
    playbackEnd: str = "playbackEnd"
    sceneExplorerNeedsUpdate: str = "sceneExplorerNeedsUpdate"
    filePostOpenProcessFinalized: str = "filePostOpenProcessFinalized"
    filePostMergeProcessFinalized: str = "filePostMergeProcessFinalized"
    preProjectFolderChange: str = "preProjectFolderChange"
    postProjectFolderChange: str = "postProjectFolderChange"
    preMxsStartupScriptLoad: str = "preMxsStartupScriptLoad"
    activeshadeInViewportToggled: str = "activeshadeInViewportToggled"
    systemShutdownCheck: str = "systemShutdownCheck"
    systemShutdownCheckFailed: str = "systemShutdownCheckFailed"
    systemShutdownCheckPassed: str = "systemShutdownCheckPassed"
    filePostMerge3: str = "filePostMerge3"
    activeshadeInFramebufferToggled: str = "activeshadeInFramebufferToggled"
    preActiveshadeInViewportToggled: str = "preActiveshadeInViewportToggled"
    postActiveshadeInViewportToggled: str = "postActiveshadeInViewportToggled"
    internalUseStart: str = "internalUseStart"
    preNewNewAll: str = "preNewNewAll"
    fileProcessScene: str = "fileProcessScene"
    fileProcessHoldFetch: str = "fileProcessHoldFetch"
    fileProcessAutobak: str = "fileProcessAutobak"
    fileStatusReadonly: str = "fileStatusReadonly"
    scenestateRename: str = "scenestateRename"
    namedSelSetRenamed: str = "namedSelSetRenamed"


def add(name: str, method: Callable, id: str = "", persistent: bool = False) -> None:
    rt.Callbacks.AddScript(rt.Name(name), method, id=rt.Name(id), persistent=persistent)


def remove(name: str, id: str = "") -> None:
    rt.Callbacks.RemoveScripts(rt.Name(name), id=rt.Name(id))
