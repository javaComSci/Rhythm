import React from 'react';
import { Button, ScrollView, StyleSheet, Text, View } from 'react-native';

export default class ProfileScreen extends React.Component {
    static navigationOptions = {
        title: 'Welcome', header: null
    };
    render() {
        return (
            <View style={styles.container}>
                <View>
                    <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> hey its ur profile screen </Text>
                </View>
                <ScrollView>
                    <Text>hello</Text>
                </ScrollView>
                <View>
                    <Button
                        title="Back"
                        onPress={() => this.props.navigation.navigate('Home')}
                    />
                </View>
            </View>
        );
    }
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#ffeceb',
        alignItems: 'center',
        justifyContent: 'center',
    },
    header: {
        height: 56 // standard for iOS devices
    }
});