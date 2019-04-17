import React from 'react';
import { Button, TextInput, TouchableHighlight, FlatList, TouchableOpacity, ScrollView, Text, View, ImageBackground, Alert } from 'react-native';
import { Audio, FileSystem } from 'expo';
import { Icon } from 'react-native-elements'
import { connect } from 'react-redux';
import DialogInput from 'react-native-dialog-input';
import RNPickerSelect from 'react-native-picker-select';
import { addEmail } from '../actions/addEmail'
import { addUser } from '../actions/addUserID';
import { addComposition } from '../actions/addComposition';
import DeleteSheetTemplate from './templates/DeleteSheetTemplate'
import DuplicateSheetTemplate from './templates/DuplicateSheetTemplate'
import NewSheetTemplate from './templates/NewSheetTemplate';
import SheetScreenTemplate from './templates/SheetScreenTemplate';
var styles = require('../style')
var background = require('../assets/backgroundImage.png')

/*
Composition class
*/
class Composition {
    constructor(title, id, description, file, instrument, tempo, author) {
        this.title = title;
        this.description = description;
        this.file = file
        this.key = id.toString(); // must be stored as string for FlatList
        this.sheetMusic = [];
        this.instrument = instrument;
        this.tempo = tempo;
        this.author = author;
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

    getTempo = function () { return this.tempo; }

    getAuthor = function () { return this.author; }
}
/* Profile Screen */
// Provides basic info regarding user's email, allows option to change given email

class ViewCompScreen extends React.Component {
    constructor(props) {
        super(props);
        console.log("props,", props);
        this.sheetList = [];
        this.compList = this.props.compositions.map(composition => ({ value: composition.key, label: composition.title, color: "red" }));
        this.compList.forEach(element => {
            if (element.value == this.props.navigation.getParam('compositionID')) {
                this.compList.splice(this.compList.indexOf(element), 1);
            }
        });
        this.state = {
            "sheet_music": [],
            newCompo: false,
            duplicateVisible: false,
            selectedSheet: null,
            selectedComposition: null,
            text: "",
            title: "",
            tempo: "",
            author: "",
            description: "",
            isDialogVisible: false,
            toEdit: '',
        }
    }

    async playSong(sheet_id) {
        await Audio.setIsEnabledAsync(true);
        const soundObject = new Audio.Sound();
        try {
            await soundObject.loadAsync({ uri: 'http://68.183.140.180:5000/getSong?sheetid=' + sheet_id });
            await soundObject.playAsync();
            // Your sound is playing!
        } catch (error) {
            // An error occurred!
            Alert.alert("No song")
        }
    }

    getInfo = function () {
        const that = this; // a reference to the previous value of "this" is required as there is a context change going into the promise of the fetch
        fetch('http://68.183.140.180:5000/getInfoBySheet', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'table': "(SELECT sheet_id,composition_id,name,song_json,instrument,tempo,author FROM sheet_music where composition_id=" + this.props.navigation.getParam('compositionID') + ") as S;--",
                'id': this.props.navigation.getParam('compositionID'),
            }),
        }).then((res) => {
            res.text().then(function (res) {
                //console.log("RES", res)
                var dummyList = [] // temp list to hold compositions before being added to state
                JSON.parse(res).forEach(element => {
                    // title, id, compid
                    // console.log(JSON.parse(element[4]))
                    dummyList.push(new Composition(element[2], element[0], element[1], JSON.parse(element[3]), element[4], element[5], element[6]));
                });
                that.setState({ "sheet_music": dummyList })
                that.sheetList = dummyList.map(sheet => ({ value: sheet.getID(), label: sheet.getTitle(), color: "red" }))
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
        this.setState({
            cameFromCamera: this.props.navigation.getParam('cameFromCamera', false)
        }, () => {
            if (this.state.cameFromCamera) {
                this.props.navigation.setParams({'compositionID': this.props.navigation.getParam('composition')})
                this.state.newCompo = true;
            }
        })
    }

    static navigationOptions = {
        title: 'Welcome', header: null
    };
    makeCompositionCall() {
        console.log("najvklafjg: ", this.props.navigation.getParam('composition'));
        fetch('http://68.183.140.180:5000/newMusicSheet', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'comp_id': this.props.navigation.getParam('compositionID'),
                'name': this.state.text,
                'tempo': this.state.tempo,
                'author': this.state.author,
            }),
        }).then((res) => {
            if (this.state.cameFromCamera) {
                this.props.navigation.state.params.onGoBack();
                this.props.navigation.goBack();
            }
            this.getInfo()
            this.state.newCompo = false;
        }).catch((res) => {
            console.log("err", res)
        });
    }

    doneComposition() {
        this.makeCompositionCall();
    }
    createComposition() {
        this.setState({
            newCompo: true,
        });
    }
    deleteComposition() {
        this.setState({
            deleteCompo: true,
        });
    }
    //{"comp_id": 146, "sheet_id": 19}
    duplicateComposition() {
        console.log("called")
        console.log(this.state.selectedComposition);
        fetch('http://68.183.140.180:5000/duplicateSheet', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'comp_id': this.state.selectedComposition,
                'sheet_id': this.state.selectedSheet,
            }),
        }).then((res) => {
            console.log("DUP res", res)
            this.setState({ duplicateVisible: false })
        }).catch((res) => {
            console.log("err", res)
        });
    }

    doneDeleteComposition() {
        deleteArr = ['name']
        deleteArr.push(this.state.deleteText)
        fetch('http://68.183.140.180:5000/delete', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'table': 'sheet_music',
                'delete': deleteArr,
            }),
        }).then((res) => {
            this.getInfo()
            this.state.deleteCompo = false;
        }).catch((res) => {
            console.log("err", res)
        });
    }

    editSheet(name, id) {
        // #  {
        //     # 	"table": "composition",
        //     # 	"update": ["name", "Chucken"],
        //     # 	"where": ["composition_id", 2]
        //     # }
        fetch('http://68.183.140.180:5000/update', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'table': 'sheet_music',
                'update': ['name', name],
                'where': ['sheet_id', id],
            }),
        }).then((res) => {
            this.getInfo();
            // this.setState({
            //     edit: false,
            //     email: this.state.emailText,
            // });
        }).catch((res) => {
            console.log("err", res)
        });
    }

    refreshFunction = () => {
        console.log("REFRESHING")
        // for (let i = 0; i < this.state.sheet_music.length; i++) {
        //     let inst = this.state.sheet_music[i].getInstrument()
        //     console.log("ISNT", inst)
        // }
        this.getInfo();
    }

    render() {
        if (this.state.deleteCompo) {
            return (
                DeleteSheetTemplate.call(this)
            );
        }
        if (this.state.duplicateVisible) {
            return (
                DuplicateSheetTemplate.call(this)
            )
        }
        if (this.state.newCompo) {
            return (
                NewSheetTemplate.call(this)
            );
        }
        // console.log("RERENDERING IN TEH VIEW COMP!")
        // console.log(this.props.navigation)
        return (
            SheetScreenTemplate.call(this)
            // <SheetScreenTemplate navigation={this.props.navigation}/>
        );
    }
};

const mapStateToProps = state => ({
    isRegistered: state.auth.isRegistered,
    id: state.auth.id,
    compositions: state.auth.compositions,
})

export default connect(mapStateToProps)(ViewCompScreen);
