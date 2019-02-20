import React from 'react';
import { TouchableOpacity, ScrollView, StyleSheet, Text, View } from 'react-native';
import { connect } from 'react-redux';

var styles = require('../style')


/* Profile Screen */
// Provides basic info regarding user's email, allows option to change given email

class ProfileScreen extends React.Component {
    constructor(props) {
        super(props);
        console.log("props,", props);
        console.log("store", this.props.store)
    }


    static navigationOptions = {
        title: 'Welcome', header: null
    };
    render() {
        return (
            <View style={styles.container}>
                <View>
                    <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 75 }}> Profile </Text>
                </View>
                <ScrollView>
                    <Text style={{ color: '#f19393', fontSize: 40 }}>Email: {this.props.isRegistered}</Text>
                </ScrollView>
                <View style={styles.footer}>
                    <TouchableOpacity
                        onPress={() => this.props.navigation.navigate('Home')}
                        style={styles.navButton}
                    >
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Home </Text>
                    </TouchableOpacity>
                </View>
            </View>
        );
    }
};

const mapStateToProps = state => ({
    isRegistered: state.auth.isRegistered,
})

export default connect(mapStateToProps)(ProfileScreen);