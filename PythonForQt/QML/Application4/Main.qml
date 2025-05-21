import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15
import QtQuick.Shapes 1.15

ApplicationWindow {
    id: mainWindow
    title: "DefectDetect Pro - Automated Inspection System"
    width: 1200
    height: 800
    minimumWidth: 800
    minimumHeight: 600
    color: "#f0f0f0"

    // Title bar
    Rectangle {
        id: titleBar
        width: parent.width
        height: 30
        color: "#404040"

        Text {
            text: mainWindow.title
            color: "white"
            font.family: "Arial"
            font.pixelSize: 14
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter
        }

        // Window controls
        Row {
            anchors.right: parent.right
            anchors.rightMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            spacing: 10

            Rectangle {
                width: 16
                height: 16
                radius: 8
                color: "#FF6058"
                border.color: "#E14942"
                border.width: 1
            }

            Rectangle {
                width: 16
                height: 16
                radius: 8
                color: "#FFBD2E"
                border.color: "#DFA123"
                border.width: 1
            }

            Rectangle {
                width: 16
                height: 16
                radius: 8
                color: "#28CA42"
                border.color: "#1AAA29"
                border.width: 1
            }
        }
    }

    // Main content area
    RowLayout {
        anchors.top: titleBar.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: statusBar.top
        spacing: 0

        // Left panel - Model Controls
        Rectangle {
            id: leftPanel
            Layout.preferredWidth: 200
            Layout.fillHeight: true
            color: "#e8e8e8"
            border.color: "#d0d0d0"
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 10

                Text {
                    text: "Model Controls"
                    font.family: "Arial"
                    font.bold: true
                    font.pixelSize: 14
                    color: "#333333"
                }

                // Model selection
                Text {
                    text: "Detection Model:"
                    font.family: "Arial"
                    font.pixelSize: 12
                    color: "#333333"
                }

                ComboBox {
                    id: modelComboBox
                    Layout.fillWidth: true
                    model: ["PCB Defect Model v2.1", "PCB Defect Model v1.8", "Custom Model"]
                    currentIndex: 0
                }

                // Confidence threshold
                Text {
                    text: "Confidence Threshold:"
                    font.family: "Arial"
                    font.pixelSize: 12
                    color: "#333333"
                }

                RowLayout {
                    Slider {
                        id: confidenceSlider
                        Layout.fillWidth: true
                        from: 0
                        to: 100
                        value: detector.confidenceThreshold
                        onValueChanged: detector.setConfidenceThreshold(value)
                    }

                    Text {
                        text: Math.round(confidenceSlider.value) + "%"
                        font.family: "Arial"
                        font.pixelSize: 12
                        color: "#333333"
                    }
                }

                // IoU threshold
                Text {
                    text: "IoU Threshold:"
                    font.family: "Arial"
                    font.pixelSize: 12
                    color: "#333333"
                }

                RowLayout {
                    Slider {
                        id: iouSlider
                        Layout.fillWidth: true
                        from: 0
                        to: 1
                        stepSize: 0.1
                        value: detector.iouThreshold
                        onValueChanged: detector.setIouThreshold(value)
                    }

                    Text {
                        text: iouSlider.value.toFixed(1)
                        font.family: "Arial"
                        font.pixelSize: 12
                        color: "#333333"
                    }
                }

                // Defect classes
                Text {
                    text: "Defect Classes:"
                    font.family: "Arial"
                    font.pixelSize: 12
                    color: "#333333"
                }

                ColumnLayout {
                    spacing: 5
                    Layout.fillWidth: true

                    CheckBox {
                        text: "Solder Defect"
                        checked: true
                        onCheckedChanged: detector.toggleDefectClass(text, checked)
                    }

                    CheckBox {
                        text: "Component Misalignment"
                        checked: true
                        onCheckedChanged: detector.toggleDefectClass(text, checked)
                    }

                    CheckBox {
                        text: "Trace Break"
                        checked: true
                        onCheckedChanged: detector.toggleDefectClass(text, checked)
                    }

                    CheckBox {
                        text: "Missing Component"
                        checked: true
                        onCheckedChanged: detector.toggleDefectClass(text, checked)
                    }
                }

                // Detection mode
                Text {
                    text: "Detection Mode:"
                    font.family: "Arial"
                    font.pixelSize: 12
                    color: "#333333"
                }

                ButtonGroup {
                    id: detectionModeGroup
                }

                ColumnLayout {
                    spacing: 5
                    Layout.fillWidth: true

                    RadioButton {
                        text: "Standard"
                        checked: detector.detectionMode === "Standard"
                        ButtonGroup.group: detectionModeGroup
                        onCheckedChanged: if (checked) detector.setDetectionMode(text)
                    }

                    RadioButton {
                        text: "High Precision"
                        checked: detector.detectionMode === "High Precision"
                        ButtonGroup.group: detectionModeGroup
                        onCheckedChanged: if (checked) detector.setDetectionMode(text)
                    }

                    RadioButton {
                        text: "High Recall"
                        checked: detector.detectionMode === "High Recall"
                        ButtonGroup.group: detectionModeGroup
                        onCheckedChanged: if (checked) detector.setDetectionMode(text)
                    }
                }

                // Run button
                Button {
                    id: runButton
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    text: "Run Detection"
                    font.bold: true
                    background: Rectangle {
                        color: "#4CAF50"
                        radius: 5
                    }
                    contentItem: Text {
                        text: runButton.text
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        font: runButton.font
                    }
                    onClicked: detector.runDetection()
                }
            }
        }

        // Center area - Image and Results
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            // Toolbar
            Rectangle {
                id: toolbar
                Layout.fillWidth: true
                Layout.preferredHeight: 40
                color: "#f5f5f5"
                border.color: "#d0d0d0"
                border.width: 1

                Row {
                    anchors.fill: parent
                    anchors.margins: 5
                    spacing: 5

                    Button {
                        width: 80
                        height: 30
                        text: "Load Image"
                        onClicked: fileDialog.open()
                    }

                    Button {
                        width: 80
                        height: 30
                        text: "Live Camera"
                    }

                    Button {
                        width: 80
                        height: 30
                        text: "Run Detection"
                        onClicked: detector.runDetection()
                    }

                    Button {
                        width: 80
                        height: 30
                        text: "Settings"
                    }

                    Button {
                        width: 90
                        height: 30
                        text: "Export Results"
                    }

                    Button {
                        width: 80
                        height: 30
                        text: "Batch Mode"
                    }

                    Button {
                        width: 80
                        height: 30
                        text: "Help"
                    }
                }
            }

            // Image display area
            Rectangle {
                id: imageContainer
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "white"
                border.color: "#d0d0d0"
                border.width: 1

                Flickable {
                    id: flickable
                    anchors.fill: parent
                    anchors.margins: 10
                    clip: true
                    contentWidth: image.width * zoomSlider.value
                    contentHeight: image.height * zoomSlider.value
                    contentX: (contentWidth - width) / 2
                    contentY: (contentHeight - height) / 2

                    Image {
                        id: image
                        source: detector.imagePath
                        width: sourceSize.width
                        height: sourceSize.height
                        transform: Scale {
                            xScale: zoomSlider.value
                            yScale: zoomSlider.value
                        }
                    }

                    // Defect overlays
                    Repeater {
                        model: detector.defects

                        Shape {
                            x: modelData.x * zoomSlider.value
                            y: modelData.y * zoomSlider.value
                            width: modelData.width * zoomSlider.value
                            height: modelData.height * zoomSlider.value

                            ShapePath {
                                strokeWidth: 2
                                strokeColor: {
                                    if (modelData.severity === "Critical") return "#ff0000";
                                    if (modelData.severity === "Medium") return "#ff9900";
                                    return "#ffcc00";
                                }
                                strokeStyle: ShapePath.DashLine
                                dashPattern: [5, 5]
                                fillColor: "transparent"
                                startX: 0; startY: 0
                                PathLine { x: width; y: 0 }
                                PathLine { x: width; y: height }
                                PathLine { x: 0; y: height }
                                PathLine { x: 0; y: 0 }
                            }

                            Text {
                                x: width / 2 - 5
                                y: height / 2 - 7
                                text: "X"
                                color: "#ff0000"
                                font.bold: true
                                font.pixelSize: 14
                            }

                            Rectangle {
                                x: width + 5
                                y: -15
                                width: 100
                                height: 25
                                color: "white"
                                border.color: "#ff0000"
                                border.width: 1

                                Text {
                                    anchors.centerIn: parent
                                    text: modelData.type
                                    color: "#ff0000"
                                    font.pixelSize: 12
                                }
                            }

                            Line {
                                x1: width
                                y1: height / 2
                                x2: width + 5
                                y2: 0
                                strokeColor: "#ff0000"
                                strokeWidth: 1
                            }
                        }
                    }
                }

                // Zoom controls
                Row {
                    anchors.bottom: parent.bottom
                    anchors.right: parent.right
                    anchors.margins: 10
                    spacing: 5

                    Slider {
                        id: zoomSlider
                        width: 150
                        from: 0.1
                        to: 3
                        value: 1
                    }

                    Button {
                        width: 25
                        height: 25
                        text: "+"
                        onClicked: zoomSlider.value = Math.min(zoomSlider.value + 0.1, zoomSlider.to)
                    }

                    Button {
                        width: 25
                        height: 25
                        text: "-"
                        onClicked: zoomSlider.value = Math.max(zoomSlider.value - 0.1, zoomSlider.from)
                    }

                    Button {
                        width: 25
                        height: 25
                        text: "↺"
                        onClicked: zoomSlider.value = 1
                    }
                }
            }

            // Results panel
            Rectangle {
                id: resultsPanel
                Layout.fillWidth: true
                Layout.preferredHeight: 200
                color: "white"
                border.color: "#d0d0d0"
                border.width: 1

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 0

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 30
                        color: "#f5f5f5"
                        border.color: "#d0d0d0"
                        border.width: 1

                        Text {
                            anchors.left: parent.left
                            anchors.leftMargin: 10
                            anchors.verticalCenter: parent.verticalCenter
                            text: "Results & Analysis"
                            font.bold: true
                            font.pixelSize: 14
                            color: "#333333"
                        }
                    }

                    TableView {
                        id: resultsTable
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        model: detector.defects
                        clip: true

                        columnWidthProvider: function(column) {
                            if (column === 0) return 50;    // ID
                            if (column === 1) return 150;   // Defect Type
                            if (column === 2) return 120;   // Location
                            if (column === 3) return 80;    // Size
                            if (column === 4) return 90;    // Confidence
                            if (column === 5) return 90;    // Severity
                            return 80;                      // Action
                        }

                        delegate: Rectangle {
                            implicitHeight: 25
                            color: row % 2 ? "#f9f9f9" : "white"
                            border.color: "#d0d0d0"
                            border.width: 1

                            Text {
                                anchors.left: parent.left
                                anchors.leftMargin: 5
                                anchors.verticalCenter: parent.verticalCenter
                                text: {
                                    if (column === 0) return modelData.id;
                                    if (column === 1) return modelData.type;
                                    if (column === 2) return "X: " + modelData.x + ", Y: " + modelData.y;
                                    if (column === 3) return modelData.width + " x " + modelData.height;
                                    if (column === 4) return modelData.confidence + "%";
                                    if (column === 5) return modelData.severity;
                                    return "";
                                }
                                color: column === 5 ?
                                    (modelData.severity === "Critical" ? "#ff0000" :
                                     modelData.severity === "Medium" ? "#ff9900" : "#ffcc00") :
                                    "#333333"
                                font.pixelSize: 12
                            }

                            Button {
                                visible: column === 6
                                anchors.centerIn: parent
                                width: 70
                                height: 18
                                text: "Details"
                                onClicked: defectDetailsDialog.showDefect(modelData)
                            }
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 25
                        color: "#e0e0e0"
                        border.color: "#d0d0d0"
                        border.width: 1

                        Row {
                            anchors.fill: parent
                            anchors.leftMargin: 10
                            spacing: 20

                            Text {
                                text: "Total Defects: " + detector.defects.length
                                font.bold: true
                                font.pixelSize: 12
                                color: "#333333"
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            Text {
                                text: "Critical: " //+ (detector.defects.filter(d => d.severity === "Critical").length
                                font.bold: true
                                font.pixelSize: 12
                                color: "#333333"
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            Text {
                                text: "Medium: " //+ (detector.defects.filter(d => d.severity === "Medium").length
                                font.bold: true
                                font.pixelSize: 12
                                color: "#333333"
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            Text {
                                text: "Low: " //+ (detector.defects.filter(d => d.severity === "Low").length
                                font.bold: true
                                font.pixelSize: 12
                                color: "#333333"
                                anchors.verticalCenter: parent.verticalCenter
                            }
                        }
                    }
                }
            }
        }

        // Right panel - Properties and Stats
        Rectangle {
            id: rightPanel
            Layout.preferredWidth: 200
            Layout.fillHeight: true
            color: "#e8e8e8"
            border.color: "#d0d0d0"
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 10

                Text {
                    text: "Properties & Stats"
                    font.family: "Arial"
                    font.bold: true
                    font.pixelSize: 14
                    color: "#333333"
                }

                // Image properties
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 120
                    color: "white"
                    border.color: "#d0d0d0"
                    border.width: 1

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 5
                        spacing: 5

                        Text {
                            text: "Image Properties"
                            font.bold: true
                            font.pixelSize: 12
                            color: "#333333"
                        }

                        Text {
                            text: "File: " + (detector.imagePath ? detector.imagePath.split("/").slice(-1)[0] : "None")
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Text {
                            text: "Size: " + (image.sourceSize.width ? image.sourceSize.width + " x " + image.sourceSize.height + " px" : "N/A")
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Text {
                            text: "Type: PCB Assembly"
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Text {
                            text: "Date: " + Qt.formatDateTime(new Date(), "yyyy-MM-dd")
                            font.pixelSize: 11
                            color: "#333333"
                        }
                    }
                }

                // Analysis statistics
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 150
                    color: "white"
                    border.color: "#d0d0d0"
                    border.width: 1

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 5
                        spacing: 5

                        Text {
                            text: "Analysis Statistics"
                            font.bold: true
                            font.pixelSize: 12
                            color: "#333333"
                        }

                        Text {
                            text: "Processing Time: " + detector.processingTime + "s"
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Text {
                            text: "Defects Found: " + detector.defects.length
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Row {
                            spacing: 5
                            Text {
                                text: "Pass/Fail:"
                                font.pixelSize: 11
                                color: "#333333"
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            Rectangle {
                                width: 50
                                height: 20
                                radius: 3
                                color: detector.defects.length > 0 ? "#ff0000" : "#28CA42"
                                Text {
                                    anchors.centerIn: parent
                                    text: detector.defects.length > 0 ? "FAIL" : "PASS"
                                    color: "white"
                                    font.pixelSize: 12
                                }
                            }
                        }

                        Text {
                            text: "Model Version: " + detector.modelVersion
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Text {
                            text: "Total Processed: 42"
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Text {
                            text: "Error Rate: 7.1%"
                            font.pixelSize: 11
                            color: "#333333"
                        }
                    }
                }

                // Selected defect
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 200
                    color: "white"
                    border.color: "#d0d0d0"
                    border.width: 1
                    visible: defectDetailsDialog.selectedDefect !== null

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 5
                        spacing: 5

                        Text {
                            text: "Selected Defect"
                            font.bold: true
                            font.pixelSize: 12
                            color: "#333333"
                        }

                        Text {
                            text: "ID: " + (defectDetailsDialog.selectedDefect ? defectDetailsDialog.selectedDefect.id : "")
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Text {
                            text: "Type: " + (defectDetailsDialog.selectedDefect ? defectDetailsDialog.selectedDefect.type : "")
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Text {
                            text: "Position: X: " + (defectDetailsDialog.selectedDefect ? defectDetailsDialog.selectedDefect.x : "") +
                                  ", Y: " + (defectDetailsDialog.selectedDefect ? defectDetailsDialog.selectedDefect.y : "")
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Text {
                            text: "Size: " + (defectDetailsDialog.selectedDefect ? defectDetailsDialog.selectedDefect.width + " x " +
                                  defectDetailsDialog.selectedDefect.height + " px" : "")
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Text {
                            text: "Area: " + (defectDetailsDialog.selectedDefect ?
                                  (defectDetailsDialog.selectedDefect.width * defectDetailsDialog.selectedDefect.height) + " sq px" : "")
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Text {
                            text: "Confidence: " + (defectDetailsDialog.selectedDefect ? defectDetailsDialog.selectedDefect.confidence + "%" : "")
                            font.pixelSize: 11
                            color: "#333333"
                        }

                        Row {
                            spacing: 5
                            Text {
                                text: "Severity:"
                                font.pixelSize: 11
                                color: "#333333"
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            Rectangle {
                                width: 60
                                height: 20
                                radius: 3
                                color: {
                                    if (!defectDetailsDialog.selectedDefect) return "transparent";
                                    if (defectDetailsDialog.selectedDefect.severity === "Critical") return "#ff0000";
                                    if (defectDetailsDialog.selectedDefect.severity === "Medium") return "#ff9900";
                                    return "#ffcc00";
                                }
                                Text {
                                    anchors.centerIn: parent
                                    text: defectDetailsDialog.selectedDefect ? defectDetailsDialog.selectedDefect.severity : ""
                                    color: "white"
                                    font.pixelSize: 12
                                }
                            }
                        }

                        Text {
                            text: "Action: " + (defectDetailsDialog.selectedDefect ? defectDetailsDialog.selectedDefect.action : "")
                            font.pixelSize: 11
                            color: "#333333"
                        }
                    }
                }

                // Defect zoom view
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 160
                    color: "white"
                    border.color: "#d0d0d0"
                    border.width: 1
                    visible: defectDetailsDialog.selectedDefect !== null

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 5

                        Text {
                            text: "Zoom View"
                            font.bold: true
                            font.pixelSize: 12
                            color: "#333333"
                            Layout.alignment: Qt.AlignHCenter
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.margins: 10
                            color: "#2d3436"
                            border.color: "#d0d0d0"
                            border.width: 1

                            Rectangle {
                                anchors.centerIn: parent
                                width: 80
                                height: 80
                                radius: width / 2
                                color: "#fd79a8"
                                border.color: "#ff0000"
                                border.width: 2

                                Text {
                                    anchors.centerIn: parent
                                    text: "X"
                                    color: "#ff0000"
                                    font.bold: true
                                    font.pixelSize: 18
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // Status bar
    Rectangle {
        id: statusBar
        anchors.bottom: parent.bottom
        width: parent.width
        height: 20
        color: "#404040"

        Text {
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            text: "Status: " + detector.statusMessage +
                  " | " + detector.defects.length + " Defects Found" +
                  " | Processing Time: " + detector.processingTime + "s" +
                  " | Ready"
            color: "white"
            font.pixelSize: 12
        }
    }

    // File dialog
    FileDialog {
        id: fileDialog
        title: "Select PCB Image"
        nameFilters: ["Image files (*.jpg *.jpeg *.png *.bmp)"]
        onAccepted: detector.loadImage(fileDialog.fileUrl.toString().replace("file:///", ""))
    }

    // Defect details dialog
    DefectDetailsDialog {
        id: defectDetailsDialog
    }
}

// Custom components
Line {
    id: line
    property color strokeColor: "black"
    property real strokeWidth: 1
    property real x1: 0
    property real y1: 0
    property real x2: 100
    property real y2: 100

    Shape {
        anchors.fill: parent
        ShapePath {
            strokeWidth: line.strokeWidth
            strokeColor: line.strokeColor
            startX: line.x1
            startY: line.y1
            PathLine { x: line.x2; y: line.y2 }
        }
    }
}

// Defect details dialog component
Component {
    id: defectDetailsDialogComponent

    Dialog {
        id: defectDetailsDialog
        property var selectedDefect: null
        modal: true
        standardButtons: Dialog.Ok
        width: 400
        height: 300

        function showDefect(defect) {
            selectedDefect = defect;
            open();
        }

        title: "Defect Details - ID: " + (selectedDefect ? selectedDefect.id : "")

        ColumnLayout {
            anchors.fill: parent
            spacing: 10

            GridLayout {
                columns: 2
                columnSpacing: 10
                rowSpacing: 5

                Text { text: "Type:"; font.bold: true }
                Text { text: selectedDefect ? selectedDefect.type : "" }

                Text { text: "Location:"; font.bold: true }
                Text {
                    text: selectedDefect ?
                          "X: " + selectedDefect.x + ", Y: " + selectedDefect.y : ""
                }

                Text { text: "Size:"; font.bold: true }
                Text {
                    text: selectedDefect ?
                          selectedDefect.width + " x " + selectedDefect.height + " px" : ""
                }

                Text { text: "Area:"; font.bold: true }
                Text {
                    text: selectedDefect ?
                          (selectedDefect.width * selectedDefect.height) + " sq px" : ""
                }

                Text { text: "Confidence:"; font.bold: true }
                Text { text: selectedDefect ? selectedDefect.confidence + "%" : "" }

                Text { text: "Severity:"; font.bold: true }
                Text {
                    text: selectedDefect ? selectedDefect.severity : ""
                    color: {
                        if (!selectedDefect) return "black";
                        if (selectedDefect.severity === "Critical") return "#ff0000";
                        if (selectedDefect.severity === "Medium") return "#ff9900";
                        return "#ffcc00";
                    }
                }

                Text { text: "Recommended Action:"; font.bold: true }
                Text { text: selectedDefect ? selectedDefect.action : "" }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 150
                color: "#f5f5f5"
                border.color: "#d0d0d0"

                Text {
                    anchors.centerIn: parent
                    text: "Defect visualization would appear here"
                    color: "#666666"
                }
            }
        }
    }
}