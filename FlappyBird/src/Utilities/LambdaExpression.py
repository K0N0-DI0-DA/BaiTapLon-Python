
from typing import Tuple


class LambdaExpression():
    """
    Được dùng chung với Callfunc (thừa kế từ Action, khi thực thi sẽ gọi hàm được gán). \n
    Các hàm ở đây là những callback dùng để thay đổi trạng thái của một node.
    """

    func_show = lambda targetNode: LambdaExpression._func_show(targetNode)
    """ Callback dùng để hiện đối tượng. """
    @staticmethod
    def _func_show(targetNode):
        targetNode.visible = True

    func_hide = lambda targetNode: LambdaExpression._func_hide(targetNode)
    """ Callback dùng để ẩn đối tượng. """
    @staticmethod
    def _func_hide(targetNode):
        targetNode.visible = False

    func_allowUpdate = lambda targetNode: LambdaExpression._func_allowUpdate(targetNode)
    """ Callback dùng để cho phép đối tượng được gọi update(). """
    @staticmethod
    def _func_allowUpdate(targetNode):
        targetNode.allowUpdate = True

    func_disallowUpdate = lambda targetNode: LambdaExpression._func_allowUpdate(targetNode)
    """ Callback dùng để chặn đối tượng gọi update(). """
    @staticmethod
    def _func_disallowUpdate(targetNode):
        targetNode.allowUpdate = False

    func_allowEventUpdate = lambda targetNode: LambdaExpression._func_allowEventUpdate(targetNode)
    """ Callback dùng để cho phép đối tượng gọi eventUpdate(). """
    @staticmethod
    def _func_allowEventUpdate(targetNode):
        targetNode.allowEventUpdate = True

    func_disallowEventUpdate = lambda targetNode: LambdaExpression._func_disallowEventUpdate(targetNode)
    """ Callback dùng để chặn đối tượng gọi eventUpdate(). """
    @staticmethod
    def _func_disallowEventUpdate(targetNode):
        targetNode.allowEventUpdate = False

    func_activate = lambda targetNode: LambdaExpression._func_activate(targetNode)
    """ Callback dùng để kích hoạt đối tượng, cho phép cập nhật và hiển thị. """
    @staticmethod
    def _func_activate(targetNode):
        targetNode.visible = True
        targetNode.allowUpdate = True
        targetNode.allowEventUpdate = True

    func_deactivate = lambda targetNode: LambdaExpression._func_deactivate(targetNode)
    """ Callback dùng để tắt đối tượng, không cho phép cập nhật và hiển thị. """
    @staticmethod
    def _func_deactivate(targetNode):
        targetNode.visible = False
        targetNode.allowUpdate = False
        targetNode.allowEventUpdate = False
    