from tkinter import *

#if Error occured with this library just delete it and set your width and height
'''from win32api import GetSystemMetrics
window_width = GetSystemMetrics(0)
window_height =  GetSystemMetrics(1)
'''
window_width = 1200
window_height =  600

# Creating Our Window and Canvas To draw on it
root = Tk()
root.geometry(f"{window_width}x{window_height}" )
root.configure(bg='light blue')
root.title("Red Black Tree")
canvas1 = Canvas(root, bg = 'light blue')

#Container To All Objects have Been Created In The Window To Manipulate or Erasing Them 
ovals = []
texts = []
lines = []


def draw_line(line_x0 ,line_y0,line_x1,line_y1, node_color):
    lines.append(canvas1.create_line(
        line_x0,
        line_y0,
        line_x1,
        line_y1,
        fill=node_color,
        width=3
        ) 
    )
    
def draw_circle(node_x0 ,node_y0,node_x1,node_y1, node_color):
    ovals.append(canvas1.create_oval(
    node_x0,
    node_y0 ,
    node_x1 , 
    node_y1,
    outline='black' , fill = node_color
    )
)

def draw_text( text_x0 , text_y0, node_value,text_color):
    texts.append(canvas1.create_text(text_x0, text_y0 , text=node_value , fill = text_color) )


def draw_node(node_x0 ,node_y0,node_x1,node_y1, node_color , text_x0 , text_y0, node_value ):
        draw_circle(node_x0 ,node_y0,node_x1,node_y1, node_color)
        draw_text( text_x0 , text_y0, node_value,'white')


def delete_all_nodes():
    for oval in ovals:
        canvas1.delete(oval)
    for text in texts :
        canvas1.delete(text)
    for line in lines:
        canvas1.delete(line)


def Add(tree , value):
    tree.insert(value)
    #Redraw Our Tree 
    delete_all_nodes()
    tree.draw_tree()
    canvas1.pack(fill=BOTH, expand=YES)
    
def Delete(tree,value):
    tree.delete_node(value)
    #Redraw Our Tree 
    delete_all_nodes()
    tree.draw_tree()
    canvas1.pack(fill=BOTH, expand=YES)


def Clear(tree):
    delete_all_nodes()
    tree.clearing()
    canvas1.pack(fill=BOTH, expand=YES)


'''def view_tree(tree):
    delete_all_nodes()
    tree.draw_tree()
    canvas1.pack(fill=BOTH, expand=YES)
'''

def draw_btns(tree):
    btns_frame = Frame(  relief = SUNKEN , borderwidth = 4  )
    btns_frame.pack()
    
    input_field = Entry(master=btns_frame, width=10,)
    add_btn = Button(   master=btns_frame, text="Add", width = 20 , command=lambda: Add( tree , int(input_field.get()) ) )
    delete_btn = Button(master=btns_frame, text="Delete", width = 20,command=lambda: Delete( tree , int(input_field.get()) ))
    # tree_view_btn = Button( master=btns_frame, text="view", width = 20,command=lambda: view_tree( tree ))
    
    add_btn.grid(row=0, column=0)
    input_field.grid(row=0, column=1)
    delete_btn.grid(row=0 , column =2 )
    # tree_view_btn.grid(row=0,column = 3)
    
    clear_btn = Button(root , text = "Clear" , command=lambda: Clear( tree ))
    clear_btn.pack(side = BOTTOM )
    
     
class Node():
    def __init__(self, data):
        self.data = data  
        self.parent = None 
        self.left = None 
        self.right = None 
        self.color = 1 


class RedBlackTree():
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL
    
    def clearing(self):
        self.root = self.TNULL
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
    
        
    def __fix_delete(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left 

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def __delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.__fix_delete(x)
    
    def  __fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left 
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right 

                if u.color == 1:
                    # mirror case 3.1
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent 
                else:
                    if k == k.parent.right:
                        # mirror case 3.2.2
                        k = k.parent
                        self.left_rotate(k)
                    # mirror case 3.2.1
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0
     
    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    def successor(self, x):

        if x.right != self.TNULL:
            return self.minimum(x.right)

        y = x.parent
        while y != self.TNULL and x == y.right:
            x = y
            y = y.parent
        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def is_exist_helper(self, node ,key):
        if node != self.TNULL:
            if key > node.data :
                return self.is_exist_helper(node.right , key)
            elif key < node.data:
                return self.is_exist_helper(node.left , key)
            else :
                return True
        else :
            return False
        
    def is_exist(self , key):
        if self.root == self.TNULL :
            return False
        
        return self.is_exist_helper(self.root,key)
    
    def insert(self, key):    
        if self.is_exist(key) == False:    
            node = Node(key)
            node.parent = None
            node.data = key
            node.left = self.TNULL
            node.right = self.TNULL
            node.color = 1 

            y = None
            x = self.root

            while x != self.TNULL:
                y = x
                if node.data < x.data:
                    x = x.left
                else:
                    x = x.right

            node.parent = y
            if y == None:
                self.root = node
            elif node.data < y.data:
                y.left = node
            else:
                y.right = node

            if node.parent == None:
                node.color = 0
                return

            if node.parent.parent == None:
                return

            self.__fix_insert(node)

    def get_root(self):
        return self.root

    def delete_node(self, data):
        self.__delete_node_helper(self.root, data)

        
    def draw_tree_helper(self, node,  level_of_node , number_of_node ):
         first_node = window_width / 2**(level_of_node+1)
         height_per_level = 70 + (80 * level_of_node)
         
         if node != self.TNULL:
            s_color = "red4" if node.color == 1 else "black"
            
            #draw Current Node
            draw_node(
                    first_node - 20 + (first_node * 2 * number_of_node),
                    height_per_level,
                    first_node + 20 + (first_node * 2 * number_of_node),
                    height_per_level + 40 ,
                    s_color,
                    first_node + (first_node * 2 * number_of_node), 
                    height_per_level + 20 ,
                    node.data
            )
            #Line to Left Child
            draw_line( 
                first_node - 20 + (first_node * 2 * number_of_node),
                height_per_level + 20 ,
                first_node / 2  + ( first_node * number_of_node * 2 ),
                height_per_level + 80 ,
                'deepskyblue4'
            )
            #Line to Right Child
            draw_line( 
                first_node / 2 + ( first_node * ( (number_of_node * 2) + 1 ) ) ,
                height_per_level + 80 ,
                first_node + 20 + (first_node * 2 * number_of_node),
                height_per_level + 20 ,
                'deepskyblue4'
            )
            
            self.draw_tree_helper(node.left, level_of_node + 1 ,  number_of_node *2 )
            self.draw_tree_helper(node.right, level_of_node + 1 , (number_of_node *2 )+ 1)
         else :
            # Drawing NIL Values
            draw_text(first_node + (first_node * 2 * number_of_node),
                height_per_level + 20 ,
                "NIL",
                'grey10'
            )

  
    def draw_tree(self ):
        if self.root != self.TNULL:
            self.draw_tree_helper(self.root,  0 , 0  )
        
if __name__ == "__main__":
    tree = RedBlackTree()
    draw_btns(tree)
    root.mainloop()
