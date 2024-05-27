# Attempting to recreate the flowchart generation after refining the structure
import graphviz


def generate_flowchart():
    dot = graphviz.Digraph(comment='Flowchart')
    dot.attr(fontname='SimHei')

    # Define nodes
    dot.node('A', '开始', shape='oval')
    dot.node('B', '存在状态为运行的进程?', shape='diamond')
    dot.node('C', '等待队列中有阻塞?', shape='diamond')
    dot.node('D', '阻塞进程进入就绪队列', shape='parallelogram')
    dot.node('E', '就绪队列有进程?', shape='diamond')
    dot.node('F', '报警', shape='parallelogram')
    dot.node('G', '设置进程P状态为运行', shape='parallelogram')
    dot.node('H', 'P运行时间未超时?', shape='diamond')
    dot.node('I', 'P执行一次', shape='parallelogram')
    dot.node('J', '出现执行异常?', shape='diamond')
    dot.node('K', 'P进入阻塞队列', shape='parallelogram')
    dot.node('L', 'P执行完成?', shape='diamond')
    dot.node('M', 'P进入完成队列', shape='parallelogram')
    dot.node('N', '设置P状态为完成', shape='parallelogram')

    # Define edges
    dot.edge('A', 'B')
    dot.edge('B', 'C', label='是')
    dot.edge('B', 'E', label='否')
    dot.edge('C', 'D', label='是')
    dot.edge('C', 'E', label='否')
    dot.edge('E', 'F', label='否')
    dot.edge('E', 'G', label='是')
    dot.edge('G', 'H')
    dot.edge('H', 'I', label='否')
    dot.edge('H', 'A', label='是')
    dot.edge('I', 'J')
    dot.edge('J', 'K', label='是')
    dot.edge('J', 'L', label='否')
    dot.edge('L', 'M', label='是')
    dot.edge('L', 'N', label='否')
    dot.edge('M', 'A')
    dot.edge('N', 'A')

    return dot


if __name__ == '__main__':
    flowchart = generate_flowchart()
    flowchart.render('temp', format='png', cleanup=False)
