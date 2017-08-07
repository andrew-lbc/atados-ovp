
"""
class MutatorWatcher(type):
  def __init__(klass, name, bases, attr_dict):
    if len(klass.mro()) > 2:
      print("was subclassed by " + name)
    return super().__init__(name, bases, attr_dict)

class AbstractMutator(metaclass=MutatorWatcher):
  pass
  """
  class AutoInput(metaclass=MutatorWatcher):
    def __init__(klass, name, bases, attr_dict):
      pass
  """

class ModelMutation(AbstractMutator):
  pass