import React from 'react';
import { Alert, TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View, KeyboardAvoidingView, ImageBackground } from 'react-native';
import { connect } from 'react-redux';
import { Header } from 'react-navigation';
import { Audio } from 'expo';
import { addEmail } from '../actions/addEmail'
import { addUser } from '../actions/addUserID';
import { addComposition } from '../actions/addComposition';
import NewCompTemplate from './templates/NewCompTemplate'
import DeleteCompTemplate from './templates/DeleteCompTemplate'
import CompScreenTemplate from './templates/CompScreenTemplate'
var styles = require('../style');
var background = require('../assets/backgroundImage.png')

/*
todo: get compositions from database
*/

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

class CompositionScreen extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            "compositions": [],
            newCompo: false,
            text: "",
            description: "",
            deleteCompo: false,
            isDialogVisible: false,
            deleteText: "",
            toEdit: "",
            cameFromCamera: false, // flag
        }
    }
    static navigationOptions = {
        title: 'Welcome', header: null
    };

    async playSong(comp_id) {
        await Audio.setIsEnabledAsync(true);
        const soundObject = new Audio.Sound();
        try {
            await soundObject.loadAsync({ uri: 'http://68.183.140.180:5000/getSong?compid=' + comp_id });
            await soundObject.playAsync();
            // Your sound is playing!
        } catch (error) {
            // An error occurred!
            Alert.alert("No song")
        }
    }

    getInfo = function () {
        const that = this; // a reference to the previous value of "this" is required as there is a context change going into the promise of the fetch
        console.log("USER ID:", that.props.id)
        fetch('http://68.183.140.180:5000/getInfo', {
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
                that.setState({ "compositions": dummyList })
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
                this.state.newCompo = true;
            }
        })
    }

    componentDidMount() {
    }

    makeCompositionCall() {
        const that = this;
        fetch('http://68.183.140.180:5000/newComposition', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'id': that.props.id,
                'description': this.state.description,
                'name': this.state.text,
            }),
        }).then((res) => {
            console.log("res: ", res)
            if (this.state.cameFromCamera) {
                this.props.navigation.state.params.onGoBack();
                this.props.navigation.goBack();
            }
            that.getInfo()
            that.state.newCompo = false;
        }).catch((res) => {
            console.log("err", res)
        });
    }

    duplicateComposition(newName) {
        const that = this;
        params = {
            'user_id': parseInt(that.props.id),
            'title': newName,
            'comp_id': parseInt(that.state.toEdit[1]),
        }
        fetch('http://68.183.140.180:5000/duplicateComposition', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params),
        }).then((res) => {
            that.getInfo()
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

    doneDeleteComposition() {
        deleteArr = ['name']
        const that = this;
        deleteArr.push(this.state.deleteText)
        fetch('http://68.183.140.180:5000/delete', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'table': 'composition',
                'delete': deleteArr,
            }),
        }).then((res) => {
            that.getInfo()
            that.state.deleteCompo = false;
        }).catch((res) => {
            console.log("err", res)
        });
    }

    render() {
        if (this.state.deleteCompo == true) {
            return (
                DeleteCompTemplate.call(this)
            );
        }
        if (this.state.newCompo == true) {
            return (
                NewCompTemplate.call(this)
            );
        }
        return (
            CompScreenTemplate.call(this)
        );
    }
};

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

export default connect(mapStateToProps, mapDispatchToProps)(CompositionScreen);