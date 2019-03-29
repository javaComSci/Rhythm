import React from 'react';
import { ListItem, Dimensions, TextInput, TouchableOpacity, ScrollView, StyleSheet, View, Text, KeyboardAvoidingView, Image, ImageBackground } from 'react-native';
// import { Header } from 'react-navigation';
import { connect } from 'react-redux';
import { Button, Header } from 'react-native-elements';
import PinchZoomView from 'react-native-pinch-zoom-view';

var styles = require('../style')

class ViewExportScreen extends React.Component{

	constructor(props) {
		super(props);

		this.state = {
			sheet_ids: this.props.navigation.getParam('sheet_ids'),
			email: this.props.navigation.getParam('email'),
		}
	}

	static navigationOptions = {
    	title: 'Welcome', header: null
  	};

  	exportSheets = () => {
  		console.log("HERE")
  		console.log(this.state.sheet_ids)
  		console.log(this.state.email)
  		if (this.state.email != '') {
            // has entered email
            console.log("IN HERE");
            fetch('http://18.237.79.152:5000/createPDF', {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                	'sheet_ids': this.state.sheet_ids,
                	'email': this.state.email,
                }),
            }).then((res) => {
                this.props.navigation.navigate('EditMusicScreen')
            }).catch((res) => {
                console.log("err", res)
            });
        }
  	}

	render() {

		return (
			  <ImageBackground style={{ width: '100%', height: '100%' }}>
	            <View>
	                <View></View>
	                <View>
	                    <View>
	                    	<Text style = {{fontSize: 45, marginTop: '50%', fontWeight: 'bold', color: 'black', textAlign: 'center'}}> Export to Email</Text>
	                    	<View style={{margin: '10%'}}>
		                        <TextInput style={{ height: 50, width: '100%', borderColor: 'gray', borderWidth: 2, borderRadius: 2}}
		                        	onChangeText={(email) => this.setState({email})}
		 							value={this.state.email}/>
		 					</View>
	                        <TouchableOpacity style={{backgroundColor: 'black', marginTop: '5%'}} onPress={() => this.exportSheets()}>
	                            <Text style={{ color: 'white', fontSize: 30, textAlign: 'center' }}>Send Email</Text>
	                        </TouchableOpacity>
	                    </View>
	                </View>
	            </View>
	            <View style={{marginTop: '80%'}}>
                    <TouchableOpacity
                        onPress={() => this.props.navigation.navigate('ViewCompScreen')}
                        style={styles.navButton}
                    >
                        <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 40 }}> Back </Text>
                    </TouchableOpacity>
                </View>
	        </ImageBackground>
		);
	}

}


export default ViewExportScreen

