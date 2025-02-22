import bpy
from bpy.types import (Panel,
                       Operator,
                       )
from bpy.props import (BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       )

from batoms.utils.butils import get_selected_objects, get_selected_batoms
from batoms import Batoms

# The panel.
class Bond_PT_prepare(Panel):
    bl_label       = "Bond"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = "Batoms"
    bl_idname = "BATOMS_PT_Bond"

  
    def draw(self, context):
        layout = self.layout
        bbpanel = context.scene.bbpanel

        layout.label(text="Bond style")
        col = layout.column()
        col.prop(bbpanel, "bond_style", expand  = True)
        layout.prop(bbpanel, "min")
        layout.prop(bbpanel, "max")
        layout.prop(bbpanel, "bondwidth")

        layout.prop(bbpanel, "order")
        layout.prop(bbpanel, "order_offset")

        layout.prop(bbpanel, "search")
        layout.prop(bbpanel, "polyhedra")
        layout.operator("bond.remove")
        layout.operator("bond.add")

        layout.prop(bbpanel, "bondcolor")

class BondProperties(bpy.types.PropertyGroup):
    @property
    def selected_batoms(self):
        return get_selected_batoms()
    @property
    def selected_bond(self):
        return get_selected_objects('bbond')
    def Callback_bond_style(self, context):
        bbpanel = bpy.context.scene.bbpanel
        bond_style = list(bbpanel.bond_style)[0]
        modify_bond_attr(self.selected_batoms, self.selected_bond, 'style', bond_style)
    def Callback_modify_min(self, context):
        bbpanel = bpy.context.scene.bbpanel
        min = bbpanel.min
        modify_bond_attr(self.selected_batoms, self.selected_bond, 'min', min)
    def Callback_modify_max(self, context):
        bbpanel = bpy.context.scene.bbpanel
        max = bbpanel.max
        modify_bond_attr(self.selected_batoms, self.selected_bond, 'max', max)
    def Callback_modify_bondwidth(self, context):
        bbpanel = bpy.context.scene.bbpanel
        bondwidth = bbpanel.bondwidth
        modify_bond_attr(self.selected_batoms, self.selected_bond, 'width', bondwidth)
    def Callback_modify_search(self, context):
        bbpanel = bpy.context.scene.bbpanel
        search = bbpanel.search
        modify_bond_attr(self.selected_batoms, self.selected_bond, 'search', search)
    def Callback_modify_polyhedra(self, context):
        bbpanel = bpy.context.scene.bbpanel
        polyhedra = bbpanel.polyhedra
        modify_bond_attr(self.selected_batoms, self.selected_bond, 'polyhedra', polyhedra)
    def Callback_modify_bondcolor(self, context):
        bbpanel = bpy.context.scene.bbpanel
        bondcolor = bbpanel.bondcolor
        modify_bond_attr(self.selected_batoms, self.selected_bond, 'color', bondcolor)
    def Callback_modify_order(self, context):
        bbpanel = bpy.context.scene.bbpanel
        order = bbpanel.order
        modify_bond_attr(self.selected_batoms, self.selected_bond, 'order', order)
    def Callback_modify_order_offset(self, context):
        bbpanel = bpy.context.scene.bbpanel
        order_offset = bbpanel.order_offset
        modify_bond_attr(self.selected_batoms, self.selected_bond, 'order_offset', order_offset)

    bond_style: EnumProperty(
        name="style",
        description="bond style",
        items=(('0',"Unicolor cylinder", ""),
               ('1',"Bicolor cylinder", ""),
               ('2',"Dashed line", ""),
               ('3',"Dotted line", "")),
        default={'1'},
        update=Callback_bond_style,
        options={'ENUM_FLAG'},
        )
    bondwidth: FloatProperty(
        name="bondwidth", default=0.1,
        description = "bondwidth", update = Callback_modify_bondwidth)
    min: FloatProperty(
        name="Length min", default=0,
        description = "min", update = Callback_modify_min)
    max: FloatProperty(
        name="Length max", default=2.0,
        description = "max", update = Callback_modify_max)
    search: IntProperty(name="Search mode", default=0, 
                update = Callback_modify_search)
    polyhedra: BoolProperty(name="polyhedra", default=False, 
                update = Callback_modify_polyhedra)
    bondcolor: FloatVectorProperty(
        name="bondcolor", 
        subtype='COLOR',
        default=(0.1, 0.8, 0.4 ,1.0),
        size =4,
        description="color picker",
        update = Callback_modify_bondcolor)
    order: IntProperty(name="Bond order", default=1, 
                update = Callback_modify_order)
    order_offset: FloatProperty(name="order_offset", default=0.15, 
                update = Callback_modify_order_offset)

def modify_bond_attr(selected_batoms, selected_bond, key, value):
    selected_bond_new = []
    for batoms_name in selected_batoms:
        batoms = Batoms(label = batoms_name)
        for bond_name in selected_bond:
            bond = bpy.data.objects[bond_name]
            if bond.batoms.bbond.label == batoms_name:
                if key != 'color':
                    setattr(batoms.bondsetting['%s-%s'%(bond.batoms.bbond.species1, 
                        bond.batoms.bbond.species2)], key, value)
                else:
                    index = [bond.batoms.bbond.species1, bond.batoms.bbond.species2].index(bond.batoms.bbond.species) + 1
                    setattr(batoms.bondsetting['%s-%s'%(bond.batoms.bbond.species1, 
                            bond.batoms.bbond.species2)], 'color%s'%index, value)
                if batoms.bondsetting['%s-%s'%(bond.batoms.bbond.species1, bond.batoms.bbond.species2)].style == '0':
                    selected_bond_new.append('%s_bond_%s_%s'%(bond.batoms.bbond.label, 
                        bond.batoms.bbond.species1, bond.batoms.bbond.species2))
                else:
                    selected_bond_new.append('%s_bond_%s_%s_%s'%(bond.batoms.bbond.label, 
                        bond.batoms.bbond.species1, bond.batoms.bbond.species2, bond.batoms.bbond.species))
        batoms.draw()
    for name in selected_bond_new:
        obj = bpy.data.objects.get(name)
        obj.select_set(True)     

def remove(selected_batoms, selected_bond):
    selected_bond_new = []
    for batoms_name in selected_batoms:
        batoms = Batoms(label = batoms_name)
        for bond_name in selected_bond:
            bond = bpy.data.objects[bond_name]
            if bond.batoms.bbond.label == batoms_name:
                batoms.bondsetting.remove([bond.batoms.bbond.species1, 
                        bond.batoms.bbond.species2])
        batoms.draw()

def add_bond(selected_batoms, selected_batom):
    selected_bond_new = []
    for batoms_name in selected_batoms:
        batoms = Batoms(label = batoms_name)
        species_list = []
        for batom_name in selected_batom:
            batom = bpy.data.objects[batom_name]
            if batom.batom.label == batoms_name:
                species_list.append(batom.batom.species)
        if len(species_list) == 1:
            batoms.bondsetting.add([species_list[0], species_list[0]])
        elif len(species_list) == 2:
            batoms.bondsetting.add([species_list[0], species_list[1]])
        elif len(species_list) > 2:
            raise Exception('Please select only two atoms')
        batoms.draw()

class RemoveButton(Operator):
    bl_idname = "bond.remove"
    bl_label = "Remove"
    bl_description = "Remove selected atoms"

    @property
    def selected_batoms(self):
        return get_selected_batoms()
    @property
    def selected_bond(self):
        return get_selected_objects('bbond')
    

    def execute(self, context):
        remove(self.selected_batoms, self.selected_bond)
        return {'FINISHED'}

class AddButton(Operator):
    bl_idname = "bond.add"
    bl_label = "Add"
    bl_description = "Add selected atoms"

    @property
    def selected_batoms(self):
        return get_selected_batoms()
    @property
    def selected_batom(self):
        return get_selected_objects('batom')
    

    def execute(self, context):
        add_bond(self.selected_batoms, self.selected_batom)
        return {'FINISHED'}
