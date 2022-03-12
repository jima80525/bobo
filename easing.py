from textual._easing import EASING
from textual.app import App
from textual.reactive import Reactive

from textual.views import DockView
from textual.widgets import Placeholder, TreeControl, ScrollView, TreeClick, TreeNode

authors = ["me", "myself", "I"]

class EasingApp(App):
    """An app do demonstrate easing."""

    side = Reactive(False)
    easing = Reactive("linear")

    def watch_side(self, side: bool) -> None:
        self.log("JIMA HIT WATCH SIDE")

    async def on_load(self, event):
        await self.bind("q", "quit")

    async def on_mount(self) -> None:
        """Called when application mode is ready."""

        self.placeholder = Placeholder()
        self.easing_view = DockView()
        self.placeholder.style = "white on dark_blue"

        tree = TreeControl("Easing", {})
        for easing_key in sorted(authors):
            # ttt = TreeNode(tree.root, tree.id, tree._tree, tree, easing_key, {"mykey": "myval"})
            #      self.root: TreeNode[NodeDataType] = TreeNode(
            #None, self.id, self, self._tree, label, data
            #            parent: TreeNode[NodeDataType] | None,
            #node_id: NodeID,
            #control: TreeControl,
            #tree: Tree,
            #label: TextType,
            #data: NodeDataType,
            #)
            await tree.add(tree.root.id, easing_key, {"easing":
                                                      easing_key.upper()})
            await tree.add(ttt)
        await tree.root.expand()

        await self.view.dock(ScrollView(tree), edge="left", size=32)
        await self.view.dock(self.easing_view)
        await self.easing_view.dock(self.placeholder, edge="left", size=32)

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        """Called in response to a tree click."""
        self.easing = message.node.data.get("easing", "linear")
        self.log("JIMA MESSAGE", message)
        self.side = not self.side


EasingApp().run(log="textual.log")
