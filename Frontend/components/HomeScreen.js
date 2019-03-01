import React from 'react';
import { connect } from 'react-redux';
import { Alert, AsyncStorage, TouchableOpacity, ScrollView, StyleSheet, Text, View } from 'react-native';
import RegisterScreen from './RegisterScreen';
import { ImagePicker, Permissions } from 'expo';
import { addEmail } from '../actions/addEmail'
import { addUser } from '../actions/addUserID';
var styles = require('../style')

/*
todo: load generated music files from local storage
todo:
*/

class HomeScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
            userEmail: null,
        };
    }

    clearCache = function () {
        console.log("clearing storage");
        // clears local storage for debugging purposes

        // AsyncStorage.clear().then(() => {
        this.props.navigation.navigate("EditMusicScreen"); //Change this
        // });
        console.log("cleared");
    }

    takeAndUploadPhotoAsync = async () => {
        // Display the camera to the user and wait for them to take a photo or to cancel
        // the action
        await Permissions.askAsync(Permissions.CAMERA_ROLL);
        await Permissions.askAsync(Permissions.CAMERA);
        // changed
        let result = await ImagePicker.launchCameraAsync();


        if (result.cancelled) {
            return;
        }

        // ImagePicker saves the taken photo to disk and returns a local URI to it
        let localUri = result.uri;
        let filename = localUri.split('/').pop();

        // Infer the type of the image
        let match = /\.(\w+)$/.exec(filename);
        let type = match ? `image/${match[1]}` : `image`;

        // Upload the image using the fetch and FormData APIs
        let formData = new FormData();
        // Assume "photo" is the name of the form field the server expects
        formData.append('photo', { uri: localUri, name: filename, type });
        console.log('photo file name', filename)
        fetch("http://18.237.79.152:5000/uploadImage", {
            method: 'POST',
            //body: formData,
            body: { "name": filename, "comp_id": 1 },
            header: {
                //'content-type': 'multipart/form-data',
                'content-type': 'application/json',
            },
        }).then(result => {
            result.text().then(res => {
                console.log("camera res", res)
            }).catch(err => {
                console.log("camera err", err)
            })
        });
    }

    componentDidMount() {
        const that = this;
        AsyncStorage.getItem("email")
            .then(result => {
                console.log("storage result", result);
                this.setState({
                    isLoading: false, // set isLoading to false until item is retrieved
                    userEmail: result ? result : "none", // if result was null, set email to none
                })
                if (this.state.userEmail === 'none') {
                    this.props.navigation.navigate("Register");
                }
                else {
                    that.props.dispatchAddEmail(result);
                }
            })
            .catch(error => {
                this.setState({
                    isLoading: false,
                    userEmail: error,
                })
            })
        // store userID locally
        AsyncStorage.getItem("id")
            .then(result => {
                console.log("id res", result);
                this.setState({
                    id: result
                })
                if (result) {
                    // send ID to redux store
                    that.props.dispatchAddUser(result);
                }
            })
    }
    static navigationOptions = {
        title: '', header: null // setting header to null to remove the default header from react-navigation
    };
    render() {
        if (this.state.isLoading) {
            return <View><Text>Loading...</Text></View>
        }
        else if (!this.state.userEmail)
            return <View><Text>Loading...</Text></View>
        return (
            <View style={styles.container}>
                <ScrollView>
                    <View style={styles.textHolder}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 75 }}> Rhythm </Text>
                    </View>
                </ScrollView>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.props.navigation.navigate('Composition')} style={styles.navButton}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Compositions </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.props.navigation.navigate('Profile')} style={styles.navButton}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Profile </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.takeAndUploadPhotoAsync()} style={styles.navButton}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Camera </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.clearCache()} style={styles.navButton}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Clear Cache </Text>
                    </TouchableOpacity>
                </View>
            </View>
        );
    }
};

function mapStateToProps(state) {
    return {
        isRegistered: state.email,
        id: state.id,
    }
}

function mapDispatchToProps(dispatch) {
    return {
        dispatchAddEmail: email => dispatch(addEmail(email)),
        dispatchAddUser: id => dispatch(addUser(id)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(HomeScreen);
