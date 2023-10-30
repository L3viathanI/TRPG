from typing import Any
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

VALUE_TYPES = ["num", "alpha", "bool"]
TARGETS = ["self", "st", "mt"]
OPERATORS = ["+", "*", "="]
COMPARISON =["=", "!=", ">", ">=", "<", "<="]

NumType = int | float

@dataclass
class FlatChangeStruct:
    modifier: str
    value: NumType

@dataclass
class AttrBasedValStruct:
    attribute: str
    attribute_owner: str
    modifier: str | None
    value: NumType | None
    flat: FlatChangeStruct | None

SupportedValTypes = int | float | str | bool | AttrBasedValStruct

@dataclass
class AttrValueStruct:
    attribute: str
    type: str
    value: SupportedValTypes

@dataclass
class ConditionStruct:
    attribute: str
    attribute_owner: str
    comparison: str
    value: SupportedValTypes

@dataclass
class EffectStruct:
    attribute: str
    effect_type: str
    condition: str
    modifier: str
    value: SupportedValTypes
    condition: ConditionStruct | None

@dataclass
class EventEndConditionStruct:
    comparison: str
    value: int

@dataclass
class EventEndConditionAttributeStruct:
    obj: str
    attribute: str
    comparison: str
    value: SupportedValTypes

@dataclass
class EventSpeechStruct:
    speaker: str
    text: str

@dataclass
class EventActionStruct:
    user: str
    action: str
    target: Sequence[str]

class TAttribute:
    def __init__(self,
                 name: str,
                 value_type: str):
        """Initialize a new TAttribute member

        Args:
            name (str): Name of the attribute
            value_type (str): Value type of the attribute. Must be "num", "alpha" or "bool", representing numerical, alphabetic or boolean data
        """
        self._name = name
        self._value_type = value_type

        self.update_data()
        
    def update_data(self):
        """A method to make sure data in self.data corresponds with instance properties
        """
        self.data = {"name": self._name,
                     "value type": self._value_type}
    

    def get_name(self) -> str:
        """Returns the name of the attribute.

        Returns:
            str: The attribute's name
        """
        return self._name

    def get_value_type(self) -> str:
        """Returns value type of the attribute

        Returns:
            str: The attribute's value type
        """
        return self._value_type
    
    def set_name(self, new_attribute_name: str):
        self._name = new_attribute_name

        self.update_data()

    def set_value_type(self, new_attribute_type: str):
        if not new_attribute_type in VALUE_TYPES:
            raise ValueError("Attribute type {} is not a supported type.\n".format(new_attribute_type))
        
        self._value_type = new_attribute_type

        self.updata_data()


class TNumAttribute(TAttribute):
    def __init__(self, name):
        super().__init__(name, "num")

class TAlphaAttribute(TAttribute):
    def __init__(self, name):
        super().__init__(name, "alpha")

class TBoolAttribute(TAttribute):
    def __init__(self, name):
        super().__init__(name, "bool")

class TPercentAttribute(TAttribute):
    def __init__(self, name):
        super().__init__(name, "percent")

class TAction:
    def __init__(self,
                 name: str,
                 effects: Sequence[EffectStruct]):
        self._name = name
        self._effects: Sequence[EffectStruct] = effects
        
        self.update_data()

    def update_data(self):
        self.data = {"name": self._name,
                    "effects": []}
        
        for ele in self._effects:
            effect_data = {"attribute": ele.attribute,
                           "effect type": ele.effect_type,
                           "modifier": ele.modifier,
                           "value": None,
                           "condition": None}
            
            if isinstance(ele.value, EffectStruct):
                effect_data["value"] = {"attribute": ele.value.attribute,
                                        "attribute owner": ele.value.attribute_owner,
                                        "modifier": ele.value.modifier,
                                        "value": ele.value.value,
                                        "flat": ele.value.flat}
            else:
                effect_data["value"] = ele.value

            if isinstance(ele.condition, ConditionStruct):
                effect_data["condition"] = {"attribute": ele.condition.attribute,
                                            "attribute owner": ele.condition.attribute_owner,
                                            "comparison": ele.condition.comparison,
                                            "value": ele.condition.value}
                
            self.data["effects"].append(effect_data)

    def get_name(self) -> str:
        return self._name

    def get_effects(self) -> Sequence[EffectStruct]:
        return self._effects
    
    def set_name(self, new_action_name: str):
        self._name = new_action_name

        self.update_data()

    def set_effects(self, new_action_effects: Sequence[EffectStruct]):
        self._effects = new_action_effects

        self.update_data()

class TEntity:
    def __init__(self,
                 name: str,
                 attributes: Sequence[AttrValueStruct] = None,
                 actions: Sequence[TAction] = None):
        
        self._name = name
        self._attributes: Mapping[str: AttrValueStruct] = {}

        for ele in attributes:
            self._attributes.update({ele.attribute: ele})

        self._actions: Mapping[str: TAction] = {}


        for action in actions:
            if isinstance(action, TAction):
                self._actions.update({action.get_name(): action})

        self.update_data()
        

    def update_data(self):

        self.data = {"name": self._name,
                    "attributes": [],
                    "actions": []}
        
        for ele in self._attributes:
            self.data["attributes"].append({"name": self._attributes[ele].attribute,
                                            "value type": self._attributes[ele].type,
                                            "value": self._attributes[ele].value})

        for ele in self._actions:
            self.data["actions"].append(ele)

    def get_name(self):
        return self._name

    def get_attributes(self):
        return self._attributes
    
    def get_actions(self):
        return self._actions
    
    def set_name(self, new_action_name: str):
        self._name = new_action_name

        self.update_data()

    def set_attributes(self, new_entity_attributes: Sequence[AttrValueStruct]):
        self._attributes = new_entity_attributes

        self.update_data()

    def set_actions(self, new_entity_actions: Sequence[TAction]):
        self._actions = new_entity_actions

        self.update_data()

    def display(self, attribute_name):
        if attribute_name not in self._attridefbutes:
            raise ValueError("An attribute named {} does not exist in entity {}.\n".format(attribute_name, self._name))

        return str("{} {}: {}").format(self._name ,attribute_name, self._attributes[attribute_name].value)

    def check_condition(self,
                        condition: ConditionStruct) -> bool:
        if condition.attribute not in self._attributes:
            raise ValueError("The attribute checked by this condition {} is not an attribute in the entity {}.\n".format(condition.attribute, self._name))

        if condition.comparison == "=":
            if self._attributes[condition.attribute].value == condition.value:
                return True

            else:
                return False

        elif condition.comparison == "!=":
            if self._attributes[condition.attribute].value != condition.value:
                return True

            else:
                return False

        elif condition.comparison == ">":
            if self._attributes[condition.attribute].value > condition.value:
                return True

            else:
                return False

        elif condition.comparison == ">=":
            if self._attributes[condition.attribute].value >= condition.value:
                return True

            else:
                return False

        elif condition.comparison == "<":
            if self._attributes[condition.attribute].value < condition.value:
                return True

            else:
                return False

        elif condition.comparison == "<=":
            if self._attributes[condition.attribute].value <= condition.value:
                return True

            else:
                return False

    def get_value_based_on_attribute(self,
                                     value: AttrBasedValStruct):
        if value.attribute not in self._attributes:
            raise ValueError(
                "An attribute named {} does not exist in {}'s attribute list.\n".format(value.attribute, self._name))

        flat = 0
        if isinstance(value.flat, FlatChangeStruct):
            if value.flat.modifier == "+":
                flat = value.flat.value

            elif value.flat.modifier == "-":
                flat = -value.flat.value

        true_value = flat
        if value.modifier == "+":
            true_value += self._attributes[value.attribute].value + value.value

        elif value.modifier == "*":
            true_value += self._attributes[value.attribute].value * value.value

        return true_value

    def use_action(self, action: TAction, obj: Sequence[Any] | None) -> bool:

        if not isinstance(obj[0], TEntity):
            raise ValueError("Object type is not TEntity.\n")

        if action.get_name() not in self._actions:
            raise ValueError("An action named {} is not in {}'s action list.\n".format(action.get_name(), self._name))

        effects = action.get_effects()
        revert = self._attributes

        for effect in effects:
            if effect.effect_type == "self":
                if effect.attribute not in self._attributes:
                    self._attributes = revert
                    raise ValueError("A self-targeted effect of action {} manipulates an attribute {} that is not present in entity {}".format(action.get_name(), effect.attribute.get_name(), self._name))

                if effect.condition is not None:
                    if not self.check_condition(effect.condition):
                        self._attributes = revert
                        break

                attribute: str = effect.attribute
                value: SupportedValTypes = effect.value
                modifier: str = effect.modifier
                condition: str = effect.condition

                true_value = value

                if condition is not None:
                    if not self.check_condition(effect.condition):
                        return None

                if isinstance(value, AttrBasedValStruct):

                    if value.attribute_owner == "user":
                        true_value = self.get_value_based_on_attribute(value)

                    elif value.attribute_owner == "target":
                        if isinstance(obj[0], TEntity):
                            target = obj[0]
                            true_value = target.get_value_based_on_attribute(value)

                        else:
                            raise ValueError("An effect of action {} uses attribute based values depending on target but no valid target was given.\n".format(action.get_name()))

                if modifier == "+":
                    self._attributes[attribute].value += true_value

                elif modifier == "*":
                    self._attributes[attribute].value *= true_value
                    

                elif modifier == "=":
                    self._attributes[attribute].value = true_value
                    

            elif effect.effect_type == "st":
                if obj is None:
                    self._attributes = revert
                    raise ValueError("A single-targeted effect of action {} requires a target but none was given.\n")

                target: TEntity
                st_revert: dict[str: AttrValueStruct]

                if isinstance(obj[0], TEntity):
                    target = obj[0]
                    st_revert = target.get_attributes()

                else:
                    raise ValueError("An invalid target object was given. Expected list[TObject | TEntity] got {}".format(type(obj)))

                if effect.attribute not in target._attributes:
                    self._attributes = revert
                    target._attributes = st_revert
                    raise ValueError(
                        "A single-targeted effect of action {} manipulates an attribute {} that is not present in entity {}".format(
                            action.get_name(), effect.attribute, target.get_name()))

                if effect.condition is not None:
                    if not self.check_condition(effect.condition):
                        self._attributes = revert
                        target._attributes = st_revert
                        break

                attribute: str = effect.attribute
                value: SupportedValTypes = effect.value
                modifier: str = effect.modifier
                condition: str = effect.condition

                true_value = value

                if condition is not None:
                    if not self.check_condition(effect.condition):
                        return None

                if isinstance(value, AttrBasedValStruct):

                    if value.attribute_owner == "user":
                        true_value = self.get_value_based_on_attribute(value)

                    elif value.attribute_owner == "target":
                        if isinstance(obj[0], TEntity):
                            true_value = target.get_value_based_on_attribute(value)

                        else:
                            raise ValueError(
                                "An effect of action {} uses attribute based values depending on target but no valid target was given.\n".format(
                                    action.get_name()))

                if modifier == "+":
                    target._attributes[attribute].value += true_value
                    
                elif modifier == "*":
                    target._attributes[attribute].value *= true_value
                    
                elif modifier == "=":
                    target._attributes[attribute].value = true_value          

            elif effect.effect_type == "mt":
                if not isinstance(obj, list):
                    self._attributes = revert
                    raise ValueError("A multi-targeted effect of action {} requires a list of targets and none was given.\n".format(action.get_name()))

                if not all(isinstance(ele, TEntity) for ele in obj):
                    self._attributes = revert
                    raise ValueError("Not all elements of the list of targets given are TEntity types.\n")

                target: TEntity
                for target in obj:
                    st_revert = target.get_attributes()

                    if effect.attribute not in target.get_attributes():
                        self._attributes = revert
                        target._attributes = st_revert
                        raise ValueError(
                            "A single-targeted effect of action {} manipulates an attribute {} that is not present in entity {}".format(
                                action.get_name(), effect.attribute, target.get_name))

                    if effect.condition is not None:
                        if not self.check_condition(effect.condition):
                            self._attributes = revert
                            target._attributes = st_revert
                            break

                    attribute: str = effect.attribute
                    value: SupportedValTypes = effect.value
                    modifier: str = effect.modifier
                    condition: str = effect.condition

                    true_value = value

                    if condition is not None:
                        if not self.check_condition(effect.condition):
                            return None

                    if isinstance(value, AttrBasedValStruct):

                        if value.attribute_owner == "user":
                            true_value = self.get_value_based_on_attribute(value)

                        elif value.attribute_owner == "target":
                            if isinstance(obj[0], TEntity):
                                true_value = target.get_value_based_on_attribute(value)

                            else:
                                raise ValueError(
                                    "An effect of action {} uses attribute based values depending on target but no valid target was given.\n".format(
                                        action.get_name()))

                    if modifier == "+":
                        target._attributes[attribute].value += true_value                        

                    elif modifier == "*":
                        target._attributes[attribute].value *= true_value

                    elif modifier == "=":
                        target._attributes[attribute].value = true_value

    def get_actions(self):
        return self._actions

class TEvent:
    def __init__(self,
                 participants: Sequence[TEntity],
                 turn_definitions: list[EventActionStruct | EventSpeechStruct],
                 end_condition: EventEndConditionStruct | EventEndConditionAttributeStruct):

        self.turns: int = 0
        self.log: str
        self.end = end_condition
        self.participants: Mapping[str: TEntity]= {}
        self.turn_def = turn_definitions
        self.current_turn: EventActionStruct | EventSpeechStruct

        for ele in participants:
            self.participants.update({ele.get_name(): ele})


    def check_end(self):
        if isinstance(self.end, EventEndConditionStruct):
            if self.end.comparison == "=":
                if self.turns == self.end.value:
                    return True

                else:
                    return False

            elif self.end.comparison == "!=":
                if self.turns != self.end.value:
                    return True

                else:
                    return False

            elif self.end.comparison == ">":
                if self.turns > self.end.value:
                    return True

                else:
                    return False

            elif self.end.comparison == ">=":
                if self.turns >= self.end.value:
                    return True

                else:
                    return False

            elif self.end.comparison == "<":
                if self.turns < self.end.value:
                    return True

                else:
                    return False

            elif self.end.comparison == "<=":
                if self.turns <= self.end.value:
                    return True

                else:
                    return False

        elif isinstance(self.end, EventEndConditionAttributeStruct):
            if self.end.obj not in self.participants:
                raise ValueError("Entity {} is not a part of this event.\n".format(self.end.obj))

            if self.end.attribute not in self.participants[self.end.obj].get_attributes():
                raise ValueError("An attribute {} is not part of {}'s attribute list.\n".format(self.end.attribute, self.end.obj))

            entity = self.participants[self.end.obj]
            entity_attributes = entity.get_attributes()

            if self.end.comparison == "=":
                if entity_attributes[self.end.attribute].value == self.end.value:
                    return True

                else:
                    return False

            elif self.end.comparison == "!=":
                if entity_attributes[self.end.attribute].value != self.end.value:
                    return True

                else:
                    return False

            elif self.end.comparison == ">":
                if entity_attributes[self.end.attribute].value > self.end.value:
                    return True

                else:
                    return False

            elif self.end.comparison == ">=":
                if entity_attributes[self.end.attribute].value >= self.end.value:
                    return True

                else:
                    return False

            elif self.end.comparison == "<":
                if entity_attributes[self.end.attribute].value < self.end.value:
                    return True

                else:
                    return False

            elif self.end.comparison == "<=":
                if entity_attributes[self.end.attribute].value <= self.end.value:
                    return True

                else:
                    return False
                

class TRPG:
    def __init__(self,
                 name: str):
        self._name: str = name
        self.attributes: dict[str: TAttribute] = {}
        self.actions: dict[str: TAction] = {}
        self.entities: dict[str:TEntity] = {}
        self.event: dict[str: TEvent] = {}
        self.event_running: TEvent | None = None
        self.log: str
        self.data = {"name": self._name,
                     "attributes": [],
                     "actions": [],
                     "entities": []}        


    def get_name(self):
        return self._name

    def update_data(self):
        self.data["name"] = self._name

        self.data["attributes"] = []
        self.data["actions"] = []
        self.data["entities"] = []

        for ele in self.attributes:
            self.data["attributes"].append(self.attributes[ele].data)

        for ele in self.actions:
            self.data["actions"].append(self.actions[ele].data)

        for ele in self.entities:
            self.data["entities"].append(self.entities[ele].data)
 
    def load_data(self):
        self.attributes.clear()
        self.actions.clear()
        self.entities.clear()

        self._name = self.data["name"]

        for ele in self.data["attributes"]:
            self.new_attribute(ele["name"], ele["value type"])

        for ele in self.data["actions"]:
            effects_list = []
            for eff in ele["effects"]:
                condition = None
                if eff["condition"] != None:
                    condition = ConditionStruct(eff["condition"]["attribute"],
                                                eff["condition"]["attribute owner"],
                                                eff["condition"]["comparison"],
                                                eff["condition"]["value"])
                    
                effect = EffectStruct(eff["attribute"], eff["effect type"], condition, eff["modifier"], eff["value"])
                effects_list.append(effect)

            self.new_action(ele["name"], effects=effects_list)

        for ele in self.data["entities"]:
            attribute_list = []
            
            for attribute in ele["attributes"]:
                attribute_list.append(AttrValueStruct(attribute["name"], attribute["value type"], attribute["value"]))

            self.new_entity(ele["name"], attribute_list, ele["actions"])

    def new_attribute(self,
                      name: str,
                      value_type: str):
        if name in self.attributes:
            raise ValueError("An attribute named {} already exists in this game.\n".format(name))

        if value_type not in VALUE_TYPES:
            raise ValueError("Value type {} is not a supported value type.\n".format(value_type))

        new = TAttribute(name, value_type)

        self.attributes.update({new.get_name(): new})

        self.update_data()

    def new_action(self,
                   name: str,
                   *,
                   effects: Sequence[EffectStruct]):
        if name in self.actions:
            raise ValueError("An action named {} already exists in this game.\n".format(name))

        action_effects: list[EffectStruct] = []

        for effect in effects:
            if effect.attribute not in self.attributes:
                raise ValueError("An attribute named {} does not exist in this game.\n".format(effect.attribute))

            if effect.effect_type not in TARGETS:
                raise ValueError("Target {} is not a supported target.\n".format(effect.effect_type))

            if effect.modifier not in OPERATORS:
                raise ValueError("Operator {} is not a supported operator.\n".format(effect.modifier))

            if effect.modifier != "=" and isinstance(effect.value, (bool, str)):
                raise ValueError("Operator {} is not applicable on value of type {}.\n".format(effect.modifier, type(effect.value)))


            if effect.condition is not None:

                condition = effect.condition

                if condition.attribute not in self.attributes:
                    raise ValueError("An attribute named {} does not exist in this game.\n".format(condition.attribute))

                if condition.comparison not in COMPARISON:
                    raise ValueError("{} is not a supported comparison.\n".format(condition.comparison))

                if condition.comparison != "!=" and condition.comparison != "=" and isinstance(type(condition.value), (bool, str)):
                    raise ValueError("Comparison {} is not applicable on value of type {}.\n".format(condition.comparison, type(condition.value)))

            action_effects.append(effect)

        if len(action_effects) > 0:
            new = TAction(name, action_effects)

            self.actions.update({name: new})

            self.update_data()

    def new_entity(self,
                   name: str,
                   attributes: Sequence[AttrValueStruct],
                   actions: Sequence[str]):

        if name in self.entities:
            raise ValueError("An entity named {} already exists in this game.\n".format(name))

        object_attributes = []

        for attribute in attributes:
            if attribute.attribute not in self.attributes:
                raise ValueError("An attribute named {} does not exist in this game.\n".format(attribute.attribute))

            if attribute.type == "num" and not isinstance(attribute.value, NumType):
                raise ValueError(
                    "Value of type {} does not match attribute value type {}.\n".format(type(attribute.value),
                                                                                        attribute.type))

            if attribute.type == "alpha" and not isinstance(attribute.value, str):
                raise ValueError(
                    "Value of type {} does not match attribute value type {}.\n".format(type(attribute.value),
                                                                                        attribute.type))

            if attribute.type == "bool" and not isinstance(attribute.value, bool):
                raise ValueError(
                    "Value of type {} does not match attribute value type {}.\n".format(type(attribute.value),
                                                                                        attribute.type))

            object_attributes.append(attribute)


        object_actions = []

        for action in actions:
            if action not in self.actions:
                raise ValueError("An action named {} does not exist in this game.\n".format(action))

            object_actions.append(self.actions[action])

        if len(object_attributes) > 0 or len(object_attributes) > 0:
            new = TEntity(name, object_attributes, object_actions)

            self.entities.update({name: new})

            self.update_data()

    def new_event(self,
                     name: str,
                     participants: Sequence[str],
                     end: EventEndConditionStruct | EventEndConditionAttributeStruct):
        
        participants_list = []

        if name in self.event:
            raise ValueError("An event by this name already exists.")
        
        for ele in participants:
            if ele not in self.entities:
                raise ValueError("An entity named {} does not exist in this game.\n".format(ele))
            
            participants_list.append(self.entities[ele])

        new = TEvent(participants, end)

    def remove_attribute(self,
                         name: str):
        if name not in self.attributes:
            raise ValueError("An attribute named {} does not exist in this game.\n".format(name))

        self.attributes.pop(name)

    def remove_action(self,
                         name: str):
        if name not in self.actions:
            raise ValueError("An action named {} does not exist in this game.\n".format(name))

        self.actions.pop(name)

    def remove_entity(self,
                      name: str):
        if name not in self.entities:
            raise ValueError("An entity named {} does not exist in this game.\n".format(name))

        self.entities.pop(name)

    def remove_event(self,
                        name: str):
        if name not in self.event:
            raise ValueError("An event named {} does not exist in this game.\n".format(name))
        
        self.event.pop(name)

    def get_attribute(self,
                      name: str) -> TAttribute:
        if name not in self.attributes:
            raise ValueError("An attribute named {} does not exist in this game.\n")

        return self.attributes[name]

    def get_action(self,
                      name: str) -> TAction:
        if name not in self.actions:
            raise ValueError("An action named {} does not exist in this game.\n")

        return self.actions[name]

    def get_entity(self,
                      name: str) -> TEntity:
        if name not in self.entities:
            raise ValueError("An entity named {} does not exist in this game.\n")

        return self.entities[name]
    
    def get_event(self,
                      name: str) -> TEvent:
        if name not in self.event:
            raise ValueError("An event named {} does not exist in this game.\n")

        return self.event[name]

    def modify_attribute(self, attribute_name: str, new_attribute_name: str = None, new_attribute_type: str = None):
        if not attribute_name in self.attributes.keys():
            raise ValueError("An attribute named {} does not exist in this game.\n".format(attribute_name))
        
        attribute: TAttribute = self.attributes[attribute_name]

        if new_attribute_name is not None:
            attribute.set_name(new_attribute_name)

        if new_attribute_type is not None:
            attribute.set_value_type(new_attribute_type)

        self.update_data()

    def modify_action(self, action_name: str, new_action_name: str = None, new_action_effects: Sequence[EffectStruct] = None):
        if not action_name in self.actions.keys():
            raise ValueError("An action named {} does not exist in this game.\n".format(action_name))
        
        action: TAction = self.actions[action_name]

        if new_action_name is not None:
            action.set_name(new_action_name)

        if new_action_effects is not None:
            action_effects: list[EffectStruct] = []

            for effect in new_action_effects:
                if effect.attribute not in self.attributes:
                    raise ValueError("An attribute named {} does not exist in this game.\n".format(effect.attribute))

                if effect.effect_type not in TARGETS:
                    raise ValueError("Target {} is not a supported target.\n".format(effect.effect_type))

                if effect.modifier not in OPERATORS:
                    raise ValueError("Operator {} is not a supported operator.\n".format(effect.modifier))

                if effect.modifier != "=" and isinstance(effect.value, (bool, str)):
                    raise ValueError("Operator {} is not applicable on value of type {}.\n".format(effect.modifier, type(effect.value)))


                if effect.condition is not None:

                    condition = effect.condition

                    if condition.attribute not in self.attributes:
                        raise ValueError("An attribute named {} does not exist in this game.\n".format(condition.attribute))

                    if condition.comparison not in COMPARISON:
                        raise ValueError("{} is not a supported comparison.\n".format(condition.comparison))

                    if condition.comparison != "!=" and condition.comparison != "=" and isinstance(type(condition.value), (bool, str)):
                        raise ValueError("Comparison {} is not applicable on value of type {}.\n".format(condition.comparison, type(condition.value)))

                action_effects.append(effect)

            action.set_effects(action_effects)

        self.update_data()

    def modify_entity(self, entity_name: str, new_entity_name: str = None, new_entity_attributes: Sequence[AttrValueStruct] = None, new_entity_actions: Sequence[str] = None):
        if not entity_name in self.entitys.keys():
            raise ValueError("An entity named {} does not exist in this game.\n".format(entity_name))
        
        entity: TEntity = self.entities[entity_name]

        if new_entity_name is not None:
            entity.set_name(new_entity_name)

        if new_entity_attributes is not None:
            entity_attributes = []

            for attribute in new_entity_attributes:
                if attribute.attribute not in self.attributes:
                    raise ValueError("An attribute named {} does not exist in this game.\n".format(attribute.attribute))

                if attribute.type == "num" and not isinstance(attribute.value, NumType):
                    raise ValueError(
                        "Value of type {} does not match attribute value type {}.\n".format(type(attribute.value),
                                                                                            attribute.type))

                if attribute.type == "alpha" and not isinstance(attribute.value, str):
                    raise ValueError(
                        "Value of type {} does not match attribute value type {}.\n".format(type(attribute.value),
                                                                                            attribute.type))

                if attribute.type == "bool" and not isinstance(attribute.value, bool):
                    raise ValueError(
                        "Value of type {} does not match attribute value type {}.\n".format(type(attribute.value),
                                                                                            attribute.type))

                entity_attributes.append(attribute)
            
            entity.set_attributes(entity_attributes)

        if new_entity_actions is not None:
            entity_actions = []

            for action in new_entity_actions:
                if action not in self.actions:
                    raise ValueError("An action named {} does not exist in this game.\n".format(action))

                entity_actions.append(self.actions[action])

        self.update_data()
            
    def use_action(self,
                   user_name: str,
                   action_name: str,
                   targets: Sequence[str] | None = None):
        if user_name not in self.entities:
            raise ValueError("An entity named {} does not exist in this game.\n".format(user_name))

        if action_name not in self.actions:
            raise ValueError("An action named {} does not exist in this game.\n".format(action_name))

        user = self.get_entity(user_name)
        action = self.get_action(action_name)
        target_objects = []

        if action_name not in user.get_actions():
            raise ValueError("An action named {} is not part of {}'s action list.\n".format(action_name, user_name))

        for ele in targets:
            if ele in self.entities:
                target_objects.append(self.entities[ele])

            else:
                raise ValueError("An entity named {} does not exist in this game.\n".format(ele))

        user.use_action(action, target_objects)

        self.update_data()
      
    def start_event(self,
    
                    event_name: str):
        if event_name not in self.event:
            raise ValueError("An event named {} does not exist in this game.\n".format(event_name))
        
        if self.event_running is not None:
            raise ValueError("An event is already running.\n")

        event: TEvent = self.get_event(event_name)
        self.event_running = event



        while(event.check_end()):
            current: EventActionStruct | EventSpeechStruct = event.turn_def[event.turns]

            if isinstance(current, EventActionStruct):
                if current.user not in self.entities:
                    raise ValueError("An entity named {} does not exist in this game.\n")
                
                for ele in current.target:
                    if ele not in self.entities:
                        raise {"An entity named {} does not exist in this game.\n".format(ele)}
                    
                if current.action not in self.actions:
                    raise ValueError("An action named {} does not exist in this game.\n".format(current.action))
                
                self.use_action(current.user, current.action, current.target)

                event.log += " {} | {} used {} on {}".format(event.turns + 1,current.user, current.action, current.target)

            elif isinstance(current, EventSpeechStruct):
                if current.speaker not in self.entities:
                    raise ValueError("An entity named {} does not exist in this game.\n")
                
                event.log += "{} | {} said '{}'".format(event.turns + 1, current.speaker, current.text)

            ++event.turns

        self.event_running = None

def test_base():
    new = TRPG("Hello")

    new.new_attribute("Condition", "alpha")

    new.new_attribute("MP", "num")

    new.new_action("BOOM", effects=[EffectStruct("MP", "self", None, "=", 0), EffectStruct("Condition", "st", None, "=", "Bad")])

    new.new_entity("Keith", [AttrValueStruct("MP", "num", 30), AttrValueStruct("Condition", "alpha", "OK")], ["BOOM"])
    new.new_entity("Logan", [AttrValueStruct("MP", "num", 30), AttrValueStruct("Condition", "alpha", "OK")], ["BOOM"])

    new.use_action("Keith", "BOOM", ["Logan"])

    a: TEntity = new.entities["Keith"]
    b: TEntity = new.entities["Logan"]

    a.update_data()
    b.update_data()

    print(a.data)
    print(b.data)
