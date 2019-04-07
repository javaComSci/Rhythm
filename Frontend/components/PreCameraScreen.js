import React from 'react';
import { View, Text, ImageBackground, Alert, TouchableOpacity } from 'react-native';
import { connect } from 'react-redux';
import RNPickerSelect from 'react-native-picker-select';
import { addComposition } from '../actions/addComposition';
var styles = require('../style')
var background = require('../assets/backgroundImage.png')

/*
Composition class
*/
class Composition {
    constructor(title, description, id) {
        this.title = title;
        this.description = description;
        this.key = id.toString(); // must be stored as string for FlatList
        this.sheetMusic = [];
    }

    getTitle = function () {
        return this.title;
    }

    getID = function () {
        return this.key;
    }

    getDescription = function () {
        return this.description;
    }
}

class SheetMusic {
    constructor(title, id, description, file, instrument) {
        this.title = title;
        this.description = description;
        this.file = file
        this.key = id.toString(); // must be stored as string for FlatList
        this.sheetMusic = [];
        this.instrument = instrument;
    }

    getFile = function () {
        return this.file
    }

    getTitle = function () {
        return this.title;
    }

    getID = function () {
        return this.key;
    }

    getDescription = function () {
        return this.description;
    }

    getInstrument = function () {
        return this.instrument;
    }
}

class CameraScreen extends React.Component {
    constructor(props) {
        super(props);
        this.compList = [];
        this.sheetList = [];
        this.state = {
            "compositions": [],
            sheetList: [],
            selectedSheet: null,
            selectedComposition: null,
        };
    }

    updateActiveComposition = function (val) {
        this.setState({
            selectedComposition: val,
        }, () => {
            console.log("SELECTED COMPOSITION: ", this.state.selectedComposition)
            this.getSheet()
        })
    }

    getInfo = function () {
        const that = this; // a reference to the previous value of "this" is required as there is a context change going into the promise of the fetch
        console.log("USER ID:", that.props.id)
        fetch('http://18.237.79.152:5000/getInfo', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'table': 'composition',
                'id': that.props.id
            }),
        }).then((res) => {
            res.text().then(function (res) {
                var dummyList = [] // temp list to hold compositions before being added to state
                JSON.parse(res).forEach(element => {
                    var tempComp = new Composition(element[1], element[2], element[0]);
                    dummyList.push(tempComp);
                    that.props.dispatchAddComposition(tempComp);
                });
                that.compList = dummyList.map(composition => ({ value: composition.key, label: composition.title, color: "red" }));
                that.compList.unshift({ value: -1, label: 'New Composition...', color: "orange" })
                // this.compList.forEach(element => {
                //     // if (element.value == this.props.navigation.getParam('compositionID')) {
                //     this.compList.splice(this.compList.indexOf(element), 1);
                //     // }
                // });
                console.log("dlist:", dummyList)
                that.setState({ "compositions": dummyList })
            })
                .catch((err) => {
                    console.log("err", err)
                })
        }).catch((res) => {
            console.log("err", res)
        });
    }

    getSheet = function () {
        var that = this;
        fetch('http://18.237.79.152:5000/getInfoBySheet', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'table': "(SELECT sheet_id,composition_id,name,song_json,instrument FROM sheet_music where composition_id=" + that.state.selectedComposition + ") as S;--",
                'id': that.state.selectedComposition,
            }),
        }).then((res) => {
            res.text().then(function (res) {
                var dummyList = [] // temp list to hold compositions before being added to state
                JSON.parse(res).forEach(element => {
                    dummyList.push(new SheetMusic(element[2], element[0], element[1], JSON.parse(element[3]), element[4]));
                });
                that.setState({ "sheet_music": dummyList })
                that.sheetList = dummyList.map(sheet => ({ value: sheet.getID(), label: sheet.getTitle(), color: "red" }))
                that.setState({
                    sheetList: that.sheetList,
                })

            })
                .catch((err) => {
                    console.log("err", err)
                })
        }).catch((res) => {
            console.log("err", res)
        });
    }

    componentWillMount() {
        this.getInfo()
    }

    render() {
        const placeholder2 = {
            label: 'Select composition...',
            value: null,
            color: "gray"
        };
        const placeholder = {
            label: 'Select sheet music...',
            value: null,
            color: "gray"
        };
        return (
            <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
                <View>
                    <View>
                        <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 30, width: "80%" }}> Select composition </Text>
                    </View>
                    <View>
                        <RNPickerSelect
                            placeholder={placeholder2}
                            items={this.compList}
                            onValueChange={(value) => {
                                console.log("new value: ", value)
                                if (value == -1) {
                                    // Create new composition
                                    Alert.alert("hi");
                                }
                                this.updateActiveComposition(value)
                            }}>
                        </RNPickerSelect>
                    </View>
                    <View style={styles.lineBreak} />
                    <View>
                        <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 30, width: "80%" }}> Select sheet music </Text>
                    </View>
                    <View>
                        <RNPickerSelect
                            placeholder={placeholder}
                            items={this.state.sheetList}
                            onValueChange={(value) => {
                                this.setState({
                                    selectedSheet: value,
                                })
                            }}>
                        </RNPickerSelect>
                    </View>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.props.navigation.navigate('CameraScreen')} style={styles.navButton}>
                        <Text style={styles.menuText}> Create </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.props.navigation.navigate('Home')} style={styles.navButton}>
                        <Text style={styles.menuText}> Home </Text>
                    </TouchableOpacity>
                </View>
            </ImageBackground>
        )
    }
}

function mapStateToProps(state) {
    return {
        isRegistered: state.auth.email,
        id: state.auth.id,
        compositions: state.auth.compositions
    }
}

function mapDispatchToProps(dispatch) {
    return {
        dispatchAddEmail: email => dispatch(addEmail(email)),
        dispatchAddUser: id => dispatch(addUser(id)),
        dispatchAddComposition: composition => dispatch(addComposition(composition)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(CameraScreen);
