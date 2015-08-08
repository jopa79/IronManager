import c4d
from c4d import documents as docs


class ObjectIterator :
    def __init__(self, baseObject):
        self.baseObject = baseObject
        self.currentObject = baseObject
        self.objectStack = []
        self.depth = 0
        self.nextDepth = 0

    def __iter__(self):
        return self

    def next(self):
        if self.currentObject == None :
            raise StopIteration

        obj = self.currentObject
        self.depth = self.nextDepth

        child = self.currentObject.GetDown()
        if child :
            self.nextDepth = self.depth + 1
            self.objectStack.append(self.currentObject.GetNext())
            self.currentObject = child
        else :
            self.currentObject = self.currentObject.GetNext()
            while( self.currentObject == None and len(self.objectStack) > 0 ) :
                self.currentObject = self.objectStack.pop()
                self.nextDepth = self.nextDepth - 1
        return obj


def main():
    objsel = "Constraint"
    objcon = "Shape"
    doc = docs.GetActiveDocument()
    obj = doc.GetFirstObject()
    scene = ObjectIterator(obj)
    scene2 = ObjectIterator(obj)
    c4d.CallCommand(13957)
    
    print "START WITH THIS MADNESS!"
    c4d.CallCommand(100004766) #select all

    for obj in scene:
        print scene.depth, scene.depth*'', obj.GetName()
        if obj.GetName().find(objcon) == int(-1):
            doc.SetSelection(obj, c4d.SELECTION_SUB)
    c4d.CallCommand(12236) # Make Editable    
    c4d.CallCommand(100004766) #select all
    print "DONE FIRST!"
    
    for obj in scene2:
        print scene.depth, scene.depth*'', obj.GetName()
        if obj.GetName().find(objsel) == int(-1):
            doc.SetSelection(obj, c4d.SELECTION_SUB)
    c4d.CallCommand(12109) # Delete
    print "DONE SECOND!"
    
c4d.EventAdd


if __name__=='__main__':
    main() 
