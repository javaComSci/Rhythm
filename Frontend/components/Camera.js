import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Dimensions, Image } from 'react-native';
import { Camera, Permissions } from 'expo';
// import { Header } from 'react-navigation';
import { connect } from 'react-redux';
import { Button, Header } from 'react-native-elements';
import { Col, Row, Grid } from "react-native-easy-grid";
import Icon from 'react-native-vector-icons/AntDesign'
import PinchZoomView from 'react-native-pinch-zoom-view';
import ImgToBase64 from 'react-native-image-base64';
import { placeJson } from '../actions/placeJson';


  import { Svg } from 'expo';
  const { Circle, Rect, Path, Line, G, Defs, Use } = Svg;
  const SCREEN_WIDTH = Dimensions.get('window').width
  const SCREEN_HEIGHT = Dimensions.get('window').height

// let flag = false;

let pictureData = [];

class CameraExample extends React.Component {
  constructor(props){
    super(props);
    pictureData = [];
    // flag = false;
    this.state = {
      flag: false,
    }
  }

  state = {
    hasCameraPermission: null,
    type: Camera.Constants.Type.back,
  };

  static navigationOptions = {
      title: 'Welcome', header: null
  };

  async componentDidMount() {
    const { status } = await Permissions.askAsync(Permissions.CAMERA);
    this.setState({ hasCameraPermission: status === 'granted' });
    // composition id is this.props.target[0][0]
    // sheet music id is this.props.target[0][1]
  }

  async snapPhoto(fl) {
    console.log('Button Pressed');
    if (this.camera) {
       console.log('Taking photo');
       const options = { quality: 1, base64: true, fixOrientation: true,
       exif: true};
       await this.camera.takePictureAsync(options).then(photo => {


        // Upload the image using the fetch and FormData APIs
        let formData = new FormData();
        // Assume "photo" is the name of the form field the server expects
        formData.append('photo', { uri: photo, name: 'PHOTO.jpg', type: 'image' });
        // btoa(formData);
        // let pizzaMan = atob(formData);
        // console.log(pizzaMan);
        // console.log(formdata._parts[1])
        let uri = formData._parts[0][1].uri.base64;
        // pictureData.push(formData._parts[0][1].uri.base64);
        console.log("fl " + fl);
        if(!fl){
          console.log("HERE");
          this.setState({ flag: false })
        }
        console.log(uri);
          let isfinal = false;
          // for(let i = 0; i < pictureData.lengh; i++){
          const that = this;
            fetch('http://68.183.140.180:5000/uploadImage', {
                  method: 'POST',
                  headers: {
                      Accept: 'application/json',
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({
                    'img_data': uri,
                    'final': fl,
                    'sheetID': this.props.target[0][1] ? this.props.target[0][1] : 0,
                    'compID': this.props.target[0][0] ? this.props.target[0][0] : 0,
                  }),
              }).then((res) => {
                  console.log("I WORKED!???\n" + res)
                  that.props.dispatchPlaceJSON(res);
              }).catch((res) => {
                  console.log("err", res)
              });
        // }

        photo.exif.Orientation = 1;
       console.log("I TOOOK A PHOTO!!!")
       });
       if(fl){
         this.props.navigation.navigate('Home');
       }

     }
  }

  showButton(){
    console.log("FEAWFAEW " + this.state.flag);
    if(this.state.flag){
      console.log("Steve");
      let buttons = [];

      buttons.push(
        <TouchableOpacity
          style={{position: "absolute", top: '30%', right: '25%', alignItems: 'center', backgroundColor:"#FF8C00", borderRadius: 10, opacity:.5}}
          onPress={() => this.snapPhoto(false)}
          key="41"
        >
        <Text
        style={{fontSize:40,}}
        > Extend </Text>
        </TouchableOpacity>
      )

      buttons.push(
        <TouchableOpacity
          style={{position: "absolute", top: '50%', right: '25%', alignItems: 'center', backgroundColor:"#FF8C00", borderRadius: 10, opacity:.5}}
          onPress={() => this.snapPhoto(true)}
          key="42"
        >
        <Text
        style={{fontSize:40,}}
        > Submit </Text>
        </TouchableOpacity>
      )
      return buttons;
    }else{
      return;
    }
  }

  render() {
    const { hasCameraPermission } = this.state;
    if (hasCameraPermission === null) {
      return <View />;
    } else if (hasCameraPermission === false) {
      return <Text>No access to camera</Text>;
    } else {
      return (
        <View style={{ flex: 1 }}>
          <Camera style={{ flex: 1 }} type={this.state.type} ref={ (ref) => {this.camera = ref} }>
            <View
              style={{
                flex: 1,
                backgroundColor: 'transparent',
                flexDirection: 'row',
              }}>

              <Svg height="100%"  width="100%">
                <Rect x={SCREEN_WIDTH/25} y={SCREEN_HEIGHT/6.5} width={SCREEN_WIDTH - SCREEN_WIDTH/25 - SCREEN_WIDTH/25} height={SCREEN_HEIGHT - SCREEN_HEIGHT/6.5 - (2 * SCREEN_HEIGHT/6.5)} fill="orange" strokeWidth="2" stroke="orange" strokeOpacity=".8" fillOpacity="0" />

                <Rect x={0} y={0} width={SCREEN_WIDTH/25} height={SCREEN_HEIGHT} fill="orange" strokeWidth="0" stroke="orange" strokeOpacity=".6" fillOpacity=".2" />
                <Rect x={SCREEN_WIDTH/25} y={0} width={SCREEN_WIDTH} height={SCREEN_HEIGHT/6.5} fill="orange" strokeWidth="0" stroke="orange" strokeOpacity=".6" fillOpacity=".2" />
                <Rect x={SCREEN_WIDTH - SCREEN_WIDTH/25} y={SCREEN_HEIGHT/6.5} width={SCREEN_WIDTH} height={SCREEN_HEIGHT} fill="orange" strokeWidth="0" stroke="orange" strokeOpacity=".6" fillOpacity=".2" />
                <Rect x={SCREEN_WIDTH/25} y={SCREEN_HEIGHT - SCREEN_HEIGHT/6.5 - (1 * SCREEN_HEIGHT/6.5)} width={SCREEN_WIDTH - SCREEN_WIDTH/12.5} height={SCREEN_HEIGHT} fill="orange" strokeWidth="0" stroke="green" strokeOpacity=".6" fillOpacity=".2" />
              </Svg>
              {this.showButton()}
              <TouchableOpacity style={{
                  position: "absolute",
                  top: '77%',
                  right: '41%',
                  alignItems: 'center',
                }}
                onPress={() => this.setState({ flag: true })}
                >
                <Image style={{width: 75, height: 75}} source={require('../assets/capture.png')}
                />
              </TouchableOpacity>
            </View>
          </Camera>
        </View>
      );
    }
  }
}

function mapStateToProps(state) {
  return {
      isRegistered: state.auth.email,
      id: state.auth.id,
      compositions: state.auth.compositions,
      target: state.auth.target,
  }
}

function mapDispatchToProps(dispatch) {
  return {
      dispatchAddComposition: composition => dispatch(addComposition(composition)),
      dispatchAddTarget: target => dispatch(addTarget(target)),
      dispatchPlaceJSON: myjson => dispatch(placeJson(myjson)),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(CameraExample);
