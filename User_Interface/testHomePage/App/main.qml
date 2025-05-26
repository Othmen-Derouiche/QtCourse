import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects
import Qt.labs.settings


Window {
    id: window
    width: 1200
    height: 800
    visible: true
    title: "DefectVision AI"
    color: "transparent"
    flags: Qt.Window  //Qt.FramelessWindowHint |

    /********************  Background Image  ********************/ 
    Image {
        id: bgImage
        anchors.fill: parent
        source: "./Assets/faircraft.png"
        fillMode: Image.PreserveAspectCrop
        opacity: 0.5 // Adjust opacity as needed
        visible: true  // Explicitly set
        // Optional: Color overlay to tint the image

        onStatusChanged: {
        if (status === Image.Error) console.error("Image failed to load!");
        else if (status === Image.Ready) console.log("Image loaded successfully.");
    }
        layer.enabled: false
        layer.effect: ColorOverlay {
            color: "#f0797c" // tint (adjust as needed)
            cached: true
            opacity: 0.1
        }

    }
/*
    // Method 1 : Overlay Gradient on Top of the Image
    Rectangle {
    anchors.fill: parent
    gradient: Gradient {
        GradientStop { position: 0.0; color: "#900C3F" }
        GradientStop { position: 0.5; color: "#C70039" }
        GradientStop { position: 1.0; color: "#f0797c" }
    }
    opacity: 0.4 // Adjust to control how much the gradient affects the image
}
*/
    // Method 2 : Blend Gradient with the Image Using BlendMode
/*
    Rectangle {
    anchors.fill: parent
    gradient: Gradient {
        GradientStop { position: 0.0; color: "#900C3F" }
        GradientStop { position: 0.5; color: "#C70039" }
        GradientStop { position: 1.0; color: "#f0797c" }
    }
    layer.enabled: true
    layer.effect: Blend {
        mode: "multiply" // Other modes: "screen", "overlay", "softlight"
    }
}

*/
    // Method 3 : Use the Gradient as a Mask
/*    
    Rectangle {
    anchors.fill: parent
    gradient: Gradient {
        GradientStop { position: 0.0; color: "transparent" }
        GradientStop { position: 1.0; color: "black" }
    }
    layer.enabled: true
    layer.samplerName: "maskSource"
    layer.effect: ShaderEffect {
        property var source: bgImage
        fragmentShader: "
            uniform sampler2D source;
            uniform sampler2D maskSource;
            uniform lowp float qt_Opacity;
            varying highp vec2 qt_TexCoord0;
            void main() {
                gl_FragColor = texture2D(source, qt_TexCoord0)
                             * texture2D(maskSource, qt_TexCoord0).a
                             * qt_Opacity;
            }
        "
    }
}
*/

    // Animated pattern background
    Item {
        id: pattern
        anchors.fill: parent
        opacity: 0.05

        Canvas {
            id: canvas
            anchors.fill: parent

            onPaint: {
                var ctx = getContext("2d")
                ctx.clearRect(0, 0, width, height)

                // Draw radial pattern
                for (var x = 0; x < width; x += 60) {
                    for (var y = 0; y < height; y += 60) {
                        ctx.beginPath()
                        ctx.arc(x + 15, y + 15, 2, 0, Math.PI * 2)
                        ctx.fillStyle = "#74033e"
                        ctx.fill()
                    }
                }

                // Draw smaller radial pattern
                for (var x = 0; x < width; x += 40) {
                    for (var y = 0; y < height; y += 40) {
                        ctx.beginPath()
                        ctx.arc(x + 30, y + 30, 1, 0, Math.PI * 2)
                        ctx.fillStyle = "#ff6b6b"
                        ctx.fill()
                    }
                }
            }
        }

        // Linear gradient overlay

        Rectangle {
            anchors.fill: parent
            rotation: 45
            gradient: Gradient {
                GradientStop { position: 0.4; color: "transparent" }
                GradientStop { position: 0.5; color: "#10ffffff" }
                GradientStop { position: 0.6; color: "transparent" }
            }
        }


        // Animation
        PropertyAnimation {
            target: pattern
            property: "x"
            from: 0
            to: 60
            duration: 20000
            loops: Animation.Infinite
            running: true
        }

        PropertyAnimation {
            target: pattern
            property: "y"
            from: 0
            to: 40
            duration: 20000
            loops: Animation.Infinite
            running: true
        }
    }

    // Circuit overlay

    Rectangle {
        id: circuitOverlay
        anchors.fill: parent
        opacity: 0.3


        Canvas {
            id: circuitCanvas
            anchors.fill: parent

            onPaint: {
                var ctx = getContext("2d")
                ctx.clearRect(0, 0, width, height)

                // Horizontal lines
                for (var y = 0; y < height; y += 200) {
                    ctx.beginPath()
                    ctx.moveTo(0, y)
                    ctx.lineTo(width, y)
                    ctx.strokeStyle = "#f1e3667d"
                    ctx.lineWidth = 2
                    ctx.stroke()
                }

                // Vertical lines
                for (var x = 0; x < width; x += 150) {
                    ctx.beginPath()
                    ctx.moveTo(x, 0)
                    ctx.lineTo(x, height)
                    ctx.strokeStyle = "#f1e3667d"
                    ctx.lineWidth = 2
                    ctx.stroke()
                }
            }
        }


        // Glow animation
        SequentialAnimation on opacity {
            loops: Animation.Infinite
            running: true
            NumberAnimation { from: 0.1; to: 0.3; duration: 3000; easing.type: Easing.InOutQuad }
            NumberAnimation { from: 0.3; to: 0.1; duration: 3000; easing.type: Easing.InOutQuad }
        }
    }


    // Main content
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 30

        // Header
        ColumnLayout {
            id: header
            Layout.alignment: Qt.AlignHCenter
            spacing: 10

            Label {
                text: "DefectVision AI"
                font.pixelSize: 42
                font.bold: true
                color: "white"
                Layout.alignment: Qt.AlignHCenter

                layer.enabled: true
                layer.effect: Glow {
                    color: "#581845"
                    radius: 20
                    samples: 20
                    spread: 0.5
                }
            }

            Label {
                text: "Defect Detection Platform"
                font.pixelSize: 18
                color: "#b0bec5"
                Layout.alignment: Qt.AlignHCenter
            }
        }

        // Menu grid
        GridLayout {
            id: menuGrid
            Layout.fillWidth: true
            Layout.fillHeight: true
            //columns: width > 800 ? 5 : (width > 600 ? 3 : 1)
            //rowSpacing: 20
            //columnSpacing: 20
            columns: 3
            columnSpacing: 30
            rowSpacing: 30
            anchors.horizontalCenter: parent.horizontalCenter
            //Layout.alignment : parent.horizontalCenter

            // Menu items
            Repeater {
                model: ListModel {
                    ListElement { icon: "ℹ️"; title: "About the Project"; description: "Learn about the defect detection system "; color: "#42a5f5" }
                    ListElement { icon: "🖼️"; title: "Image Processing"; description: "Upload and preprocess images for defect analysis"; color: "#66bb6a" }
                    ListElement { icon: "🔍"; title: "Detection"; description: "Run AI model for defect detection and segmentation"; color: "#ffa726" }
                    ListElement { icon: "🔗"; title: "Benchling Integration"; description: "Connect and sync with Benchling laboratory platform"; color: "#ab47bc" }
                    ListElement { icon: "❓"; title: "Help"; description: "Documentation and support resources"; color: "#ef5350" }
                }

                delegate: Rectangle {
                    id: menuButton
                    width: 280
                    height: 180
                    //Layout.fillWidth: true
                    //Layout.fillHeight: true
                    radius: 20
                    color: Qt.rgba(1, 1, 1, 0.3)
                    border.color: Qt.rgba(1, 1, 1, 0.3)
                    border.width: 1

                    // Hover effect
                    property bool hovered: false

                    // Ripple effect
                    property point clickPos

                    ColumnLayout {
                        anchors.centerIn: parent
                        width: parent.width * 0.8
                        spacing: 15

                        Label {
                            text: model.icon
                            font.pixelSize: 48
                            Layout.alignment: Qt.AlignHCenter
                            color: model.color

                            layer.enabled: true
                            layer.effect: DropShadow {
                                color: model.color
                                radius: 10
                                samples: 20
                                spread: 0.5
                            }
                        }

                        Label {
                            text: model.title
                            font.pixelSize: 20
                            font.bold: true
                            color: "white"
                            Layout.alignment: Qt.AlignHCenter
                        }

                        Label {
                            text: model.description
                            font.pixelSize: 14
                            color: "#b0bec5"
                            wrapMode: Text.WordWrap
                            horizontalAlignment: Text.AlignHCenter
                            Layout.fillWidth: true
                        }
                    }

                    // Mouse area for interaction
                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: {
                            menuButton.hovered = true
                            hoverAnim.start()
                            borderAnim.start()
                        }
                        onExited: {
                            menuButton.hovered = false
                            hoverAnimReverse.start()
                            borderAnimReverse.start()
                        }
                        onClicked: {
                            // Create ripple effect
                            var ripple = rippleComp.createObject(menuButton, {
                                x: mouseX - 50,
                                y: mouseY - 50
                            })
                            ripple.start()
                        }
                    }

                    // Hover animation
                    PropertyAnimation {
                        id: hoverAnim
                        target: menuButton
                        property: "scale"
                        to: 1.05
                        duration: 300
                        easing.type: Easing.OutQuad
                    }

                    PropertyAnimation {
                        id: hoverAnimReverse
                        target: menuButton
                        property: "scale"
                        to: 1.0
                        duration: 300
                        easing.type: Easing.OutQuad
                    }

                    // Border color animation
                    PropertyAnimation {
                        id: borderAnim
                        target: menuButton
                        property: "border.color"
                        to: model.color
                        duration: 300
                    }

                    PropertyAnimation {
                        id: borderAnimReverse
                        target: menuButton
                        property: "border.color"
                        to: Qt.rgba(1, 1, 1, 0.2)
                        duration: 300
                    }

                    // Shine effect
                    Rectangle {
                        id: shine
                        width: parent.width * 2
                        height: parent.height
                        color: Qt.rgba(1, 1, 1, 0.1)
                        rotation: 20
                        x: -parent.width
                        y: 0
                        visible: menuButton.hovered
                    }

                    SequentialAnimation {
                        id: shineAnim
                        running: menuButton.hovered
                        loops: Animation.Infinite
                        NumberAnimation {
                            target: shine
                            property: "x"
                            from: -menuButton.width
                            to: menuButton.width
                            duration: 1500
                        }
                    }

                    // Ripple component
                    Component {
                        id: rippleComp

                        Rectangle {
                            id: ripple
                            width: 100
                            height: 100
                            radius: 50
                            color: Qt.rgba(1, 1, 1, 0.3)

                            function start() {
                                rippleAnim.start()
                            }

                            PropertyAnimation {
                                id: rippleAnim
                                target: ripple
                                property: "scale"
                                from: 0
                                to: 2
                                duration: 600
                                easing.type: Easing.OutQuad

                                onFinished: ripple.destroy()
                            }

                            PropertyAnimation {
                                target: ripple
                                property: "opacity"
                                from: 0.6
                                to: 0
                                duration: 600
                            }
                        }
                    }
                }
            }
        }
    }

    // Version info
    Label {
        anchors {
            right: parent.right
            bottom: parent.bottom
            margins: 10
        }
        text: "Version 1.0.0 | DefectVision AI Suite"
        color: Qt.rgba(1, 1, 1, 0.5)
        font.pixelSize: 12
    }

    // Drop shadow for the window
    DropShadow {
        anchors.fill: parent
        source: parent
        horizontalOffset: 0
        verticalOffset: 0
        radius: 20
        samples: 20
        color: "#80000000"
        visible: window.visible
    }
}