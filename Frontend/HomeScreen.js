import React from 'react';
import { TouchableOpacity, ScrollView, StyleSheet, Text, View } from 'react-native';

export default class HomeScreen extends React.Component {
    static navigationOptions = {
        title: 'Welcome', header: null // setting header to null removes the header
    };
    render() {
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

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#ffeceb',
    },
    textHolder: {
        height: 200,
        alignItems: 'center'
    },
    footer: {
        height: 100,
        backgroundColor: '#ffeceb',
        alignItems: 'center',
        justifyContent: 'center'
    },
    navButton: {
        height: 100,
        position: 'absolute', top: 0, bottom: 0, left: 0, right: 0,
        alignItems: 'center',
        justifyContent: 'center'
    },
});