import React from 'react';
import { connect } from 'react-redux';
import { AsyncStorage, TouchableOpacity, ScrollView, StyleSheet, Text, View } from 'react-native';
import RegisterScreen from './RegisterScreen';
import { addEmail } from '../actions/addEmail'
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

    componentDidMount() {
        const that = this;
        AsyncStorage.getItem("email")
            .then(result => {
                this.setState({
                    isLoading: false, // set isLoading to false until item is retrieved
                    userEmail: result ? result : "none", // if result was null, set email to none
                })
                if (this.state.userEmail === 'none') {
                    this.props.navigation.navigate("register");
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
            </View>
        );
    }
};

function mapStateToProps(state) {
    return {
        isRegistered: state.email
    }
}

function mapDispatchToProps(dispatch) {
    return {
        dispatchAddEmail: email => dispatch(addEmail(email))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(HomeScreen);
