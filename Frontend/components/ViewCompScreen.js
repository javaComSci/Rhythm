import React from 'react';
import { Button, TextInput, TouchableHighlight, FlatList, TouchableOpacity, ScrollView, Text, View, ImageBackground } from 'react-native';
import { Icon } from 'react-native-elements'
import { connect } from 'react-redux';
import DialogInput from 'react-native-dialog-input';
import RNPickerSelect from 'react-native-picker-select';
import { addEmail } from '../actions/addEmail'
import { addUser } from '../actions/addUserID';
import { addComposition } from '../actions/addComposition';
var styles = require('../style')
var background = require('../assets/backgroundImage.png')

/*
Composition class
*/
class Composition {
    constructor(title, id, description) {
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
                'id': this.props.navigation.getParam('compositionID'),
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
                'comp_id': this.props.navigation.getParam('compositionID'),
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
    //{"comp_id": 146, "sheet_id": 19}
    duplicateComposition() {
        console.log("called")
        console.log(this.state.selectedComposition);
        fetch('http://18.237.79.152:5000/duplicateSheet', {
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
        const placeholder = {
            label: 'Select sheet music...',
            value: null,
            color: "gray"
        };
        const placeholder2 = {
            label: 'Select composition...',
            value: null,
            color: "gray"
        };
        if (this.state.deleteCompo) {
            return (
                <View style={styles.container}>
                    <View></View>
                    <ScrollView>
                    </ScrollView>
                    <View>
                        <View style={styles.textHolder}>
                            <TextInput style={{ height: 50, width: '80%', borderColor: 'gray', borderWidth: 1 }}
                                placeholder="DeleteText"
                                onChangeText={(deleteText) => this.setState({ deleteText })}
                                value={this.state.deleteText} />
                        </View>
                        <Button onPress={() => this.doneDeleteComposition()} title="Delete Sheet Music" />
                        <View style={styles.footer}>
                            <TouchableOpacity onPress={() => this.setState({ deleteCompo: false })} style={styles.navButton}>
                                <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Back </Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                </View>
            );
        }
        //{"comp_id": 146, "sheet_id": 19}
        if (this.state.duplicateVisible) {
            return (
                <View style={styles.container}>
                    <View>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40, width: "80%" }}> Duplicate </Text>
                    </View>
                    <View>
                        <RNPickerSelect
                            placeholder={placeholder}
                            items={this.sheetList}
                            onValueChange={(value) => {
                                this.setState({
                                    selectedSheet: value,
                                })
                            }}>
                        </RNPickerSelect>
                    </View>
                    <View style={styles.lineBreak} />
                    <View>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 30, width: "80%" }}> Select composition </Text>
                    </View>
                    <View>
                        <RNPickerSelect
                            placeholder={placeholder2}
                            items={this.compList}
                            onValueChange={(value) => {
                                this.setState({
                                    selectedComposition: value,
                                })
                            }}>
                        </RNPickerSelect>
                    </View>
                    <View style={styles.footer}>
                        <TouchableOpacity onPress={() => this.duplicateComposition()} style={styles.navButton}>
                            <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Submit </Text>
                        </TouchableOpacity>
                    </View>
                    <View style={styles.footer}>
                        <TouchableOpacity onPress={() => this.setState({ duplicateVisible: false })} style={styles.navButton}>
                            <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Back </Text>
                        </TouchableOpacity>
                    </View>
                </View>
            )
        }
        if (this.state.newCompo) {
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
            <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
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
                    <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 40, width: "80%" }}> {compositionTitle} </Text>
                    <View style={styles.operatorContainer}>
                        <TouchableOpacity
                            onPress={() => this.createComposition()}
                            style={styles.addButton}
                        >
                            <Text style={styles.menuText}>+</Text>
                        </TouchableOpacity>
                        <TouchableOpacity style={styles.neutralButton} onPress={() => this.setState({ "duplicateVisible": true })}>
                            <Text style={styles.buttonText}>Duplicate</Text>
                        </TouchableOpacity>
                        <TouchableOpacity style={styles.neutralButton} onPress={() => this.props.navigation.navigate('EditMusicScreen')}>
                            <Text style={styles.buttonText}>Edit</Text>
                        </TouchableOpacity>
                        <TouchableOpacity style={styles.minusButton} onPress={() => this.deleteComposition()}>
                            <Text style={styles.menuText}>-</Text>
                        </TouchableOpacity>
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
                                                toEdit: [item.getTitle(), item.getID()], // getdescription actually gets the composition id
                                            })
                                        }}
                                    >
                                        <Text style={{ color: 'white', fontSize: 40 }}>{item.getTitle()}</Text>
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
                            <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 40 }}> Back </Text>
                        </TouchableOpacity>
                    </View>
                </View >
            </ImageBackground>
        );
    }
};

const mapStateToProps = state => ({
    isRegistered: state.auth.isRegistered,
    id: state.auth.id,
    compositions: state.auth.compositions,
})

export default connect(mapStateToProps)(ViewCompScreen);
