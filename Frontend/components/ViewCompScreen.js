import React from 'react';
import { TouchableOpacity, ScrollView, StyleSheet, Text, View } from 'react-native';
import { connect } from 'react-redux';

var styles = require('../style')


/* Profile Screen */
// Provides basic info regarding user's email, allows option to change given email

class ViewCompScreen extends React.Component {
    constructor(props) {
        super(props);
        console.log("props,", props);
    }

    static navigationOptions = {
        title: 'Welcome', header: null
    };
    render() {
        return (
            <View style={styles.container}>
                <View>
                    <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> hey its ur view specific composition screen </Text>
                </View>
                <ScrollView>
                    <Text>INNER CONTENT HERE</Text>
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

export default connect(mapStateToProps)(ViewCompScreen);