function init() {
    var $ = go.GraphObject.make;  // for conciseness in defining templates
    myDiagram =
            $(go.Diagram, "myDiagramDiv",  // must name or refer to the DIV HTML element
                    {
                        initialContentAlignment: go.Spot.Center,
                        allowDrop: true,  // must be true to accept drops from the Palette
                        "LinkDrawn": showLinkLabel,  // this DiagramEvent listener is defined below
                        "LinkRelinked": showLinkLabel,
                        "SelectionDeleting" : function(e) {
                            var it = e.subject.iterator;
                            while(it.next()) {
                                if(it.value.data.category == "Start")
                                    e.cancel = true;
                            }
                        }
                    });

    myDiagram.grid.visible = true;
    myDiagram.toolManager.draggingTool.isGridSnapEnabled = true;
    myDiagram.toolManager.resizingTool.isGridSnapEnabled = true;

    myDiagram.addDiagramListener("Modified", function(e) {
      if(myDiagram.isModified || !myDiagram.isModified && model_reload) {
        if(!myDiagram.isModified && model_reload)
            model_reload = false;
        jQuery("#edit-but a").removeClass("disabled");
      }
      else {
        jQuery("#edit-but a").addClass("disabled");
      }
    });


    // helper definitions for node templates
    function nodeStyle() {
        return [
            // The Node.location comes from the "loc" property of the node data,
            // converted by the Point.parse static method.
            // If the Node.location is changed, it updates the "loc" property of the node data,
            // converting back using the Point.stringify static method.
            new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
            {
                // the Node.location is at the center of each node
                locationSpot: go.Spot.Center,
                //isShadowed: true,
                //shadowColor: "#888",
                // handle mouse enter/leave events to show/hide the ports
                mouseEnter: function (e, obj) {
                    showPorts(obj.part, true);
                },
                mouseLeave: function (e, obj) {
                    showPorts(obj.part, false);
                }
            }
        ];
    }

    // Define a function for creating a "port" that is normally transparent.
    // The "name" is used as the GraphObject.portId, the "spot" is used to control how links connect
    // and where the port is positioned on the node, and the boolean "output" and "input" arguments
    // control whether the user can draw links from or to the port.
    function makePort(name, spot, output, input) {
        // the port is basically just a small circle that has a white stroke when it is made visible
        return $(go.Shape, "Circle",
                {
                    fill: "transparent",
                    stroke: null,  // this is changed to "white" in the showPorts function
                    desiredSize: new go.Size(8, 8),
                    alignment: spot, alignmentFocus: spot,  // align the port on the main Shape
                    portId: name,  // declare this object to be a "port"
                    fromSpot: spot, toSpot: spot,  // declare where links may connect at this port
                    fromLinkable: output, toLinkable: input,  // declare whether the user may draw links to/from here
                    cursor: "pointer"  // show a different cursor to indicate potential link point
                });
    }

    // define the Node templates for regular nodes
    var lightText = 'whitesmoke';
    myDiagram.nodeTemplateMap.add("Act",  // the default category
            $(go.Node, "Spot", nodeStyle(),
                    // the main object is a Panel that surrounds a TextBlock with a rectangular Shape
                    $(go.Panel, "Auto",
                            $(go.Shape, "Rectangle",
                                    {fill: "#00A9C9", stroke: null},
                                    new go.Binding("figure", "figure")),
                            $(go.TextBlock,
                                    {
                                        font: "bold 10pt Helvetica, Arial, sans-serif",
                                        stroke: lightText,
                                        margin: 8,
                                        maxSize: new go.Size(160, NaN),
                                        wrap: go.TextBlock.WrapFit,
                                        editable: true
                                    },
                                    new go.Binding("text").makeTwoWay())
                    ),
                    // four named ports, one on each side:
                    makePort("T", go.Spot.Top, false, true),
                    makePort("B", go.Spot.Bottom, true, false)
            ));
    myDiagram.nodeTemplateMap.add("Start",
            $(go.Node, "Spot", nodeStyle(),
                    $(go.Panel, "Auto",
                            $(go.Shape, "Circle",
                                    {minSize: new go.Size(40, 40), fill: "#79C900", stroke: null}),
                            $(go.TextBlock, "Start",
                                    {font: "bold 10pt Helvetica, Arial, sans-serif", stroke: lightText},
                                    new go.Binding("text"))
                    ),
                    makePort("B", go.Spot.Bottom, true, false)
            ));
    myDiagram.nodeTemplateMap.add("Cond",
    $(go.Node, "Spot", nodeStyle(),
            $(go.Panel, "Auto",
                    $(go.Shape, "Rectangle",
                                {fill: "#dc4a81", stroke: null},
                                new go.Binding("figure", "figure")),
                    $(go.TextBlock,
                                {
                                    font: "bold 10pt Helvetica, Arial, sans-serif",
                                    stroke: lightText,
                                    margin: 8,
                                    maxSize: new go.Size(160, NaN),
                                    wrap: go.TextBlock.WrapFit,
                                    editable: true,
                                    stroke: '#fff'
                                },
                                new go.Binding("text").makeTwoWay())
            ),
            makePort("T", go.Spot.Top, false, true),
            makePort("L", go.Spot.Left, true, false),
            makePort("R", go.Spot.Right, true, false)
    ));
    myDiagram.nodeTemplateMap.add("Out",
        $(go.Node, "Spot", nodeStyle(),
                $(go.Panel, "Auto",
                        $(go.Shape, "Output",
                                {minSize: new go.Size(100, 40), fill: "#21C47E", stroke: null}),
                        $(go.TextBlock,
                                {textAlign: "center", font: "bold 10pt Helvetica, Arial, sans-serif", stroke: lightText, editable: true},
                                new go.Binding("text").makeTwoWay())
                ),
                // four named ports, one on each side:
                makePort("T", go.Spot.Top, false, true),
                makePort("B", go.Spot.Bottom, true, false)
        ));
    myDiagram.nodeTemplateMap.add("End",
            $(go.Node, "Spot", nodeStyle(),
                    $(go.Panel, "Auto",
                            $(go.Shape, "Circle",
                                    {minSize: new go.Size(40, 40), fill: "#DC3C00", stroke: null}),
                            $(go.TextBlock, "End",
                                    {font: "bold 10pt Helvetica, Arial, sans-serif", stroke: lightText, editable: true},
                                    new go.Binding("text"))
                    ),
                    // three named ports, one on each side except the bottom, all input only:
                    makePort("T", go.Spot.Top, false, true)
            ));
    myDiagram.nodeTemplateMap.add("Comment",
            $(go.Node, "Auto", nodeStyle(),
                    $(go.Shape, "File",
                            {fill: "#EFFAB4", stroke: null}),
                    $(go.TextBlock,
                            {
                                margin: 5,
                                maxSize: new go.Size(200, NaN),
                                wrap: go.TextBlock.WrapFit,
                                textAlign: "center",
                                editable: true,
                                font: "bold 10pt Helvetica, Arial, sans-serif",
                                stroke: '#454545'
                            },
                            new go.Binding("text").makeTwoWay())
                    // no ports, because no links are allowed to connect with a comment
            ));
    // replace the default Link template in the linkTemplateMap
    myDiagram.linkTemplate =
            $(go.Link,  // the whole link panel
                    {
                        routing: go.Link.AvoidsNodes,
                        curve: go.Link.JumpOver,
                        corner: 5, toShortLength: 4,
                        relinkableFrom: true,
                        relinkableTo: true,
                        reshapable: true,
                        resegmentable: true
                    },
                    new go.Binding("points").makeTwoWay(),
                    $(go.Shape,  // the highlight shape, normally transparent
                            {isPanelMain: true, strokeWidth: 8, stroke: "transparent", name: "HIGHLIGHT"}),
                    $(go.Shape,  // the link path shape
                            {isPanelMain: true, stroke: "gray", strokeWidth: 2}),
                    $(go.Shape,  // the arrowhead
                            {toArrow: "standard", stroke: null, fill: "gray"}),
                    $(go.Panel, "Auto",  // the link label, normally not visible
                            {visible: false, name: "LABEL", segmentIndex: 2, segmentFraction: 0.5},
                            new go.Binding("visible", "visible").makeTwoWay(),
                            $(go.Shape, "RoundedRectangle",  // the label shape
                                    {fill: "#FFF", stroke: null}),
                            $(go.TextBlock, "Да",  // the label
                                    {
                                        textAlign: "center",
                                        font: "10pt helvetica, arial, sans-serif",
                                        stroke: "#333333",
                                        name: "LABEL_TEXT"
                                    },
                                    new go.Binding("text").makeTwoWay())
                    )
            );
    // Make link labels visible if coming out of a "conditional" node.
    // This listener is called by the "LinkDrawn" and "LinkRelinked" DiagramEvents.
    function showLinkLabel(e) {
        var label = e.subject.findObject("LABEL");
        var text = e.subject.findObject("LABEL_TEXT");

        if(e.subject.fromPortId == "L")
            text.text = "Нет";
        else
            text.text = "Да";

        if (label !== null) label.visible = (e.subject.fromNode.data.figure === "Diamond");
    }

    // temporary links used by LinkingTool and RelinkingTool are also orthogonal:
    myDiagram.toolManager.linkingTool.temporaryLink.routing = go.Link.Orthogonal;
    myDiagram.toolManager.relinkingTool.temporaryLink.routing = go.Link.Orthogonal;
    // initialize the Palette that is on the left side of the page
    myPalette =
            $(go.Palette, "myPaletteDiv",  // must name or refer to the DIV HTML element
                    {
                        nodeTemplateMap: myDiagram.nodeTemplateMap,  // share the templates used by myDiagram
                        model: new go.GraphLinksModel([  // specify the contents of the Palette
                            {category: "Act", text: "Действие"},
                            {category: "Cond", text: "Условие", figure: "Diamond" },
                            {category: "Out", text: "Вывод"},
                            {category: "End", text: "Конец"},
                            {category: "Comment", text: "Комментарий"}
                        ])
                    });
}
// Make all ports on a node visible when the mouse is over the node
function showPorts(node, show) {
    var diagram = node.diagram;
    if (!diagram || diagram.isReadOnly || !diagram.allowLink) return;
    node.ports.each(function (port) {
        port.stroke = (show) ? "#a0a0a0" : null;
        port.fill = (show) ? "white" : "transparent";
    });
}
