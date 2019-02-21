import React from 'react';
import { Button, TextInput, KeyboardAvoidingView, FlatList, TouchableOpacity, ScrollView, StyleSheet, Text, View } from 'react-native';
import { connect } from 'react-redux';
import DialogInput from 'react-native-dialog-input'

var styles = require('../style')

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
/* Profile Screen */
// Provides basic info regarding user's email, allows option to change given email

class ViewCompScreen extends React.Component {
    constructor(props) {
        super(props);
        console.log("props,", props);
        this.state = {
            "sheet_music": [],
            newCompo: false,
            text: "",
            description: "",
            isDialogVisible: false,
            toEdit: '',
        }
    }


    getInfo = function () {
        const that = this; // a reference to the previous value of "this" is required as there is a context change going into the promise of the fetch
        fetch('http://18.237.79.152:5000/getInfoBySheet', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'table': 'sheet_music',
                'id': 38,
            }),
        }).then((res) => {
            res.text().then(function (res) {
                console.log("RES", res)
                var dummyList = [] // temp list to hold compositions before being added to state
                JSON.parse(res).forEach(element => {
                    // title, id, compid
                    dummyList.push(new Composition(element[3], element[0], element[2]));
                });
                that.setState({ "sheet_music": dummyList })
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

    static navigationOptions = {
        title: 'Welcome', header: null
    };
    makeCompositionCall() {
        fetch('http://18.237.79.152:5000/newMusicSheet', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'comp_id': 38,
                'name': this.state.text,
            }),
        }).then((res) => {
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
        fetch('http://18.237.79.152:5000/update', {
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
                            <Button onPress={() => this.doneDeleteComposition()} title="Delete Sheet Music" />
                        </View>
                    </View>
                </View>
            );
        }

        if (this.state.newCompo == true) {
            return (
                <View style={styles.container}>
                    <View></View>
                    <ScrollView>
                    </ScrollView>
                    <View>
                        <View style={styles.textHolder}>
                            <TextInput style={{ height: 50, width: '80%', borderColor: 'gray', borderWidth: 1 }}
                                placeholder="Title"
                                onChangeText={(text) => this.setState({ text })}
                                value={this.state.text} />

                        </View>
                        <Button onPress={() => this.doneComposition()} title="Create Sheet Music" />
                        <View style={styles.footer}>
                            <TouchableOpacity onPress={() => this.setState({ newCompo: false })} style={styles.navButton}>
                                <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Back </Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                </View>
            );
        }
        const { navigation } = this.props;
        const compositionID = navigation.getParam('compositionID', 'NO_ID');
        const compositionTitle = navigation.getParam('compositionTitle', 'NO_TITLE')
        const compositionDescription = navigation.getParam('compositionDescription', '')
        return (

            <View style={styles.container}>
                <DialogInput isDialogVisible={this.state.isDialogVisible}
                    title={"Edit Sheet Name"}
                    hintInput={"New Title"}
                    submitInput={(inputText) => {
                        // edit title
                        this.editSheet(inputText, this.state.toEdit[1])
                        this.setState({ isDialogVisible: false, toEdit: '' })
                    }}
                    closeDialog={() => { this.setState({ isDialogVisible: false, toEdit: '' }) }}>
                </DialogInput>
                <View>
                    <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> {compositionTitle} </Text>
                    <Button onPress={() => this.createComposition()} title="+" />
                    <Button onPress={() => this.deleteComposition()} title="-" />
                </View>
                <Text>{compositionDescription}</Text>
                <ScrollView>
                    <FlatList
                        data={this.state.sheet_music}
                        extraData={this.state}
                        renderItem={({ item }) =>
                            <View style={styles.compositionContainer}>
                                <TouchableOpacity
                                    style={styles.compositionItem}
                                    onLongPress={(e) => {
                                        console.log("pepper")
                                        this.setState({
                                            isDialogVisible: true,
                                            toEdit: [item.getTitle(), item.getDescription()], // getdescription actually gets the composition id
                                        })
                                    }}
                                >
                                    <Text style={{ color: '#f19393', fontSize: 40 }}>{item.getTitle()}</Text>
                                </TouchableOpacity>
                                <View style={styles.lineBreak} />
                            </View>}
                    />
                </ScrollView>
                <View style={styles.footer}>
                    <TouchableOpacity
                        onPress={() => this.props.navigation.navigate('Composition')}
                        style={styles.navButton}
                    >
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Back </Text>
                    </TouchableOpacity>
                </View>
            </View>
        );
    }
};

const mapStateToProps = state => ({
    isRegistered: state.auth.isRegistered,
    id: state.auth.id,
})

export default connect(mapStateToProps)(ViewCompScreen);