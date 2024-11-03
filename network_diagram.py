import matplotlib.pyplot as plt
import networkx as nx

# Create the directed graph for the project
G_detailed = nx.DiGraph()

# Add major tasks from WBS and Gantt chart
G_detailed.add_nodes_from([
    "Project Management Plan", "Hardware Procurement", "Installation of Hardware",
    "Software Development", "Small-Scale Trial", "Large-Scale Trial", "Full Deployment",
    "System Testing", "Project Closure and Handover",
    "Hardware Site Surveys", "CCTV Installation", "Thermal Camera Setup", "API Development",
    "Mobile App", "Data Encryption", "Data Backup", "Quality Assurance", "Software Testing",
    "Integration Testing", "Final Data Insights", "System Documentation", "Contract Sign-off"
])

# Define dependencies between tasks
G_detailed.add_edges_from([
    ("Project Management Plan", "Hardware Procurement"),
    ("Project Management Plan", "Software Development"),
    ("Hardware Procurement", "Installation of Hardware"),
    ("Installation of Hardware", "CCTV Installation"),
    ("Installation of Hardware", "Thermal Camera Setup"),
    ("CCTV Installation", "Small-Scale Trial"),
    ("Thermal Camera Setup", "Small-Scale Trial"),
    ("Software Development", "API Development"),
    ("API Development", "Mobile App"),
    ("Mobile App", "Small-Scale Trial"),
    ("Small-Scale Trial", "Large-Scale Trial"),
    ("Large-Scale Trial", "Full Deployment"),
    ("Full Deployment", "System Testing"),
    ("System Testing", "Quality Assurance"),
    ("System Testing", "Software Testing"),
    ("Software Testing", "Integration Testing"),
    ("Integration Testing", "Project Closure and Handover"),
    ("Data Encryption", "Full Deployment"),
    ("Data Backup", "Full Deployment"),
    ("Final Data Insights", "Project Closure and Handover"),
    ("System Documentation", "Project Closure and Handover"),
    ("Contract Sign-off", "Project Closure and Handover")
])

# Draw the network diagram
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G_detailed, k=0.8)
nx.draw(G_detailed, pos, with_labels=True, node_size=3000, node_color="lightgreen", font_size=10, font_weight='bold', arrows=True)
plt.title('Detailed Network Diagram for TfNSW Platform Occupancy Project')
plt.show()
