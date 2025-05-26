import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt5Compat.GraphicalEffects

Window {
    visible: true
    width: 1280
    height: 720
    title: "DefectVision AI"
    color: "transparent"

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#0c1445" }
            GradientStop { position: 0.5; color: "#1a237e" }
            GradientStop { position: 1.0; color: "#3949ab" }
        }

        // Background Pattern Simulation
        Rectangle {
            anchors.fill: parent
            opacity: 0.1
            rotation: 45
            Rectangle {
                width: 100; height: 100
                color: "transparent"
                border.color: "#00ff88"
                border.width: 1
                radius: 2
                anchors.centerIn: parent
            }
        }

        // Circuit Overlay Simulation
        Rectangle {
            anchors.fill: parent
            opacity: 0.2
            layer.enabled: true
            layer.effect: OpacityMask {
                maskSource: Gradient {
                    GradientStop { position: 0.4; color: "#00ff88" }
                    GradientStop { position: 0.6; color: "#ffffff00" }
                }
            }
        }

        Column {
            anchors.centerIn: parent
            spacing: 40
            width: parent.width * 0.9

            Column {
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 10

                Text {
                    text: "DefectVision AI"
                    font.pixelSize: 42
                    font.bold: true
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Text {
                    text: "Advanced Defect Detection & Segmentation Platform"
                    font.pixelSize: 18
                    color: "#b0bec5"
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            GridLayout {
                columns: 3
                columnSpacing: 30
                rowSpacing: 30
                anchors.horizontalCenter: parent.horizontalCenter

                Repeater {
                    model: [
                        { icon: "ℹ️", title: "About the Project", desc: "Learn about our AI-powered defect detection system and its capabilities", color: "#42a5f5" },
                        { icon: "🖼️", title: "Image Processing", desc: "Upload and preprocess images for defect analysis", color: "#66bb6a" },
                        { icon: "🔍", title: "Detection", desc: "Run AI models for defect detection and segmentation", color: "#ffa726" },
                        { icon: "🔗", title: "Benchling Integration", desc: "Connect and sync with Benchling laboratory platform", color: "#ab47bc" },
                        { icon: "❓", title: "Help", desc: "Documentation, tutorials, and support resources", color: "#ef5350" }
                    ]

                    delegate: Rectangle {
                        width: 280
                        height: 180
                        radius: 20
                        border.color: modelData.color
                        color: "#ffffff10"
                        border.width: 1
                        layer.enabled: true
                        layer.effect: DropShadow {
                            color: "#00000088"
                            radius: 10
                            samples: 16
                            horizontalOffset: 0
                            verticalOffset: 4
                        }

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: parent.scale = 1.05
                            onExited: parent.scale = 1.0
                            cursorShape: Qt.PointingHandCursor
                        }

                        Column {
                            anchors.centerIn: parent
                            spacing: 8
                            Text {
                                text: modelData.icon
                                font.pixelSize: 36
                                color: modelData.color
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                            Text {
                                text: modelData.title
                                font.pixelSize: 18
                                color: "white"
                                font.bold: true
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                            Text {
                                text: modelData.desc
                                font.pixelSize: 12
                                color: "#b0bec5"
                                wrapMode: Text.WordWrap
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                    }
                }
            }
        }

        Text {
            text: "Version 1.0.0 | DefectVision AI Suite"
            font.pixelSize: 12
            color: "#ffffff80"
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.rightMargin: 20
            anchors.bottomMargin: 10
        }
    }
}
