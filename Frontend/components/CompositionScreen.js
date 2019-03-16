import React from 'react';
import { TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View, KeyboardAvoidingView, ImageBackground } from 'react-native';
import { connect } from 'react-redux';
import { Header } from 'react-navigation';
import DialogInput from 'react-native-dialog-input';
import { addEmail } from '../actions/addEmail'
import { addUser } from '../actions/addUserID';
import { addComposition } from '../actions/addComposition';
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
        }
    }
    static navigationOptions = {
        title: 'Welcome', header: null
    };

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
    }

    componentDidMount() {
    }

    makeCompositionCall() {
        const that = this;
        fetch('http://18.237.79.152:5000/newComposition', {
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
            this.getInfo()
            this.state.newCompo = false;
        }).catch((res) => {
            console.log("err", res)
        });
    }

    duplicateComposition(newName) {
        const that = this;
        fetch('http://18.237.79.152:5000/duplicateComposition', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'user_id': that.props.id,
                'title': newName,
                'comp_id': this.state.toEdit[1],
            }),
        }).then((res) => {
            this.getInfo()
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
        deleteArr.push(this.state.deleteText)
        fetch('http://18.237.79.152:5000/delete', {
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
            this.getInfo()
            this.state.deleteCompo = false;
        }).catch((res) => {
            console.log("err", res)
        });
    }

    render() {
        if (this.state.deleteCompo == true) {
            return (
                <View style={styles.container}>
                    <View>
                        <View style={styles.textHolder}>
                            <TextInput style={{ marginTop: 200, height: 50, width: '80%', borderColor: 'gray', borderWidth: 1 }}
                                placeholder="DeleteText"
                                onChangeText={(deleteText) => this.setState({ deleteText })}
                                value={this.state.deleteText} />
                            <Button onPress={() => this.doneDeleteComposition()} title="Delete Composition" />
                        </View>
                    </View>
                </View>
            );
        }
        if (this.state.newCompo == true) {
            return (
                <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
                    <View style={styles.container}>
                        <View></View>
                        <ScrollView>
                        </ScrollView>
                        <View>
                            <KeyboardAvoidingView keyboardVerticalOffset={-500} behavior="padding" style={styles.textHolder} enabled>
                                <TextInput style={{ height: 50, width: '80%', borderColor: 'gray', borderWidth: 1 }}
                                    placeholder="Title"
                                    onChangeText={(text) => this.setState({ text })}
                                    value={this.state.text} />
                                <TextInput style={{ height: 50, width: '80%', borderColor: 'gray', borderWidth: 1 }}
                                    placeholder="Description"
                                    onChangeText={(description) => this.setState({ description })}
                                    value={this.state.description} />
                                <Button onPress={() => this.doneComposition()} title="Create Composition" />
                            </KeyboardAvoidingView>
                            <View style={styles.footer}>
                                <TouchableOpacity onPress={() => this.setState({ newCompo: false })} style={styles.navButton}>
                                    <Text style={{ color: 'white', fontSize: 40 }}> Back </Text>
                                </TouchableOpacity>
                            </View>
                        </View>
                    </View>
                </ImageBackground>
            );
        }
        return (
            <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
                <View style={styles.container}>
                    <DialogInput isDialogVisible={this.state.isDialogVisible}
                        title={"Duplicate Composition"}
                        hintInput={"New Composition Name"}
                        submitInput={(inputText) => {
                            // edit title
                            // duplicate composition
                            this.duplicateComposition(inputText)
                            this.setState({ isDialogVisible: false, toEdit: '' })
                        }}
                        closeDialog={() => { this.setState({ isDialogVisible: false, toEdit: '' }) }}>
                    </DialogInput>
                    <View style={styles}>
                        <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 40 }}> COMPOSITIONS </Text>
                        <View style={styles.lineBreak} />
                    </View>
                    <View style={styles.operatorContainer}>
                        <TouchableOpacity
                            onPress={() => this.createComposition()}
                            style={styles.addButton}
                        >
                            <Text style={styles.menuText}>+</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            onPress={() => this.deleteComposition()}
                            style={styles.minusButton}
                        >
                            <Text style={styles.menuText}>-</Text>
                        </TouchableOpacity>
                    </View>
                    <ScrollView>
                        <FlatList
                            data={this.state.compositions}
                            extraData={this.state}
                            renderItem={({ item }) =>
                                <View style={styles.compositionContainer}>
                                    <TouchableOpacity
                                        onPress={() => this.props.navigation.navigate('ViewCompScreen', { 'compositionID': item.getID(), 'compositionTitle': item.getTitle(), 'compositionDescription': item.getDescription() })}
                                        style={styles.compositionItem}
                                        onLongPress={(e) => {
                                            this.setState({
                                                isDialogVisible: true,
                                                toEdit: [item.getTitle(), item.getID()], // getdescription actually gets the composition id
                                            })
                                        }}>
                                        <Text style={{ color: 'white', fontSize: 40 }}>{item.getTitle()}</Text>
                                    </TouchableOpacity>
                                    <View style={styles.lineBreak} />
                                </View>}
                        />
                    </ScrollView>
                    <View style={styles.footer}>
                        <TouchableOpacity onPress={() => this.props.navigation.navigate('Home')} style={styles.navButton}>
                            <Text style={styles.menuText}> Home </Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </ImageBackground>
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