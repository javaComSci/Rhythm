import React from 'react';
import { TouchableOpacity, ScrollView, StyleSheet, Text, View, Button, KeyboardAvoidingView, TextInput, ImageBackground } from 'react-native';
import { connect } from 'react-redux';
import ProfileScreenTemplate from './templates/ProfileScreenTemplate'
import ProfileEditTemplate from './templates/ProfileEditTemplate'
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
                ProfileEditTemplate.call(this)
            );
        }

        return (
            ProfileScreenTemplate.call(this)
        );
    }
};

const mapStateToProps = state => ({
    isRegistered: state.auth.isRegistered,
    id: state.auth.id
})

export default connect(mapStateToProps)(ProfileScreen);
