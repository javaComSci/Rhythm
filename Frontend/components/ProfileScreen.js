import React from 'react';
import { TouchableOpacity, ScrollView, StyleSheet, Text, View, Button, KeyboardAvoidingView, TextInput, ImageBackground } from 'react-native';
import { connect } from 'react-redux';

var styles = require('../style')
var background = require('../assets/backgroundImage.png')

/* Profile Screen */
// Provides basic info regarding user's email, allows option to change given email

class ProfileScreen extends React.Component {
    constructor(props) {
        super(props);
        console.log("props,", props);
        console.log("store", this.props.store)
        this.state = {
            edit: false,
            emailText: "",
            email: "",
            name: "",
            nameText: "",
        };
    }


    static navigationOptions = {
        title: 'Welcome', header: null
    };

    getInfo = function () {
        const that = this; // a reference to the previous value of "this" is required as there is a context change going into the promise of the fetch
        fetch('http://18.237.79.152:5000/getInfo', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'table': 'user',
                'id': this.props.id
            }),
        }).then((res) => {
            res.text().then(function (res) {
                let stuff = JSON.parse(res);
                that.setState({
                    email: stuff[0][1],
                    name: stuff[0][3]
                });
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

    editProfile() {
        this.setState({
            edit: true,
        });
    }

    makeEditCall() {
        if (this.state.nameText == '' && this.state.emailText != '') {
            // only email, no name
            updateInfo = ['email']
            updateInfo.push(this.state.emailText);
            fetch('http://18.237.79.152:5000/update', {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'table': 'user',
                    'update': updateInfo,
                    'where': ['user_id', this.props.id],
                }),
            }).then((res) => {
                this.setState({
                    edit: false,
                    email: this.state.emailText,
                });
            }).catch((res) => {
                console.log("err", res)
            });
        } else if (this.state.nameText != '' && this.state.emailText == '') {
            // only name, no email
            updateInfo = ['name'];
            updateInfo.push(this.state.nameText);
            fetch('http://18.237.79.152:5000/update', {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'table': 'user',
                    'update': updateInfo,
                    'where': ['user_id', this.props.id],
                }),
            }).then((res) => {
                this.setState({
                    edit: false,
                    name: this.state.nameText,
                });
            }).catch((res) => {
                console.log("err", res)
            });
        } else if (this.state.nameText != '' && this.state.emailText != '') {
            updateInfo = ['email']
            updateInfo.push(this.state.emailText);
            updateInfo.push('name');
            updateInfo.push(this.state.nameText);
            fetch('http://18.237.79.152:5000/updateMulti', {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'table': 'user',
                    'update': updateInfo,
                    'where': ['user_id', this.props.id],
                }),
            }).then((res) => {
                this.setState({
                    edit: false,
                    name: this.state.nameText,
                    email: this.state.emailText,
                });
            }).catch((res) => {
                console.log("err", res)
            });
        }
    }

    doneEdit() {
        console.log("EDIT CALL");
        this.makeEditCall();
    }

    render() {
        if (this.state.edit == true) {
            return (
                <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
                    <View style={styles.container}>
                        <View>
                            <KeyboardAvoidingView keyboardVerticalOffset={-500} behavior="padding" style={styles.textHolder} enabled>
                                <TextInput style={{ marginTop: '70%', height: 40, width: '90%', borderColor: '#f19393', borderWidth: 1, fontWeight: 'bold', }}
                                    placeholder="Name"
                                    onChangeText={(nameText) => this.setState({ nameText })}
                                    value={this.state.nameText} />
                                <TextInput style={{ marginTop: 10, height: 40, width: '90%', borderColor: '#f19393', borderWidth: 1, fontWeight: 'bold', }}
                                    placeholder="Email"
                                    onChangeText={(emailText) => this.setState({ emailText })}
                                    value={this.state.emailText} />
                            </KeyboardAvoidingView>
                            <View style={styles.footer}>
                                <TouchableOpacity
                                    style={styles.navButton}
                                    onPress={() => this.doneEdit()}
                                >
                                    <Text style={{ color: 'white', fontSize: 40 }}> Submit </Text>
                                </TouchableOpacity>
                            </View>
                            <View style={styles.footer}>
                                <TouchableOpacity
                                    onPress={() => { this.setState({ edit: false, }) }}
                                    style={styles.navButton}
                                >
                                    <Text style={{ color: 'white', fontSize: 40 }}> Cancel </Text>
                                </TouchableOpacity>
                            </View>
                        </View>
                    </View >
                </ImageBackground>
            );
        }

        return (
            <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
                <View style={styles.container}>
                    <View>
                        <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 75 }}> Profile </Text>
                    </View>
                    <ScrollView style={{ flex: 1, marginLeft: 50 }}>
                        <Text style={{ color: 'white', fontSize: 40 }}>{this.state.name ? this.state.name != '' : "Unnamed"} </Text>
                        <Text style={{ color: 'white', fontSize: 20 }}>{this.state.email} </Text>
                    </ScrollView>
                    <View style={styles.footer}>
                        <TouchableOpacity
                            onPress={() => this.editProfile()}
                            style={styles.navButton}
                        >
                            <Text style={{ color: 'white', fontSize: 40 }}> Edit </Text>
                        </TouchableOpacity>
                    </View>
                    <View style={styles.footer}>
                        <TouchableOpacity
                            onPress={() => this.props.navigation.navigate('Home')}
                            style={styles.navButton}
                        >
                            <Text style={{ color: 'white', fontSize: 40 }}> Home </Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </ImageBackground>
        );
    }
};

const mapStateToProps = state => ({
    isRegistered: state.auth.isRegistered,
    id: state.auth.id
})

export default connect(mapStateToProps)(ProfileScreen);
