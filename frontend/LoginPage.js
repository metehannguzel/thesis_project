import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { useNavigation } from '@react-navigation/native';



const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigation = useNavigation(); 

    const handleLogin = () => {
        console.log('Kullanıcı Adı:', username);
        console.log('Parola:', password);
        navigation.navigate('Camera'); 
    };
    const handleSignup = () => {
        navigation.navigate('Signup'); 
    }

    return (
        <View style={styles.container}>
            <View style={styles.pageWrapper}>
                <View style={styles.contentWrapper}>
                    <View style={styles.row}>
                        <View style={styles.col}>
                            <View style={styles.form}>
                                <View style={styles.logoContainer}>
                                    
                                    
                                </View>
                                <Text style={styles.title}>Let's Start!</Text>
                                <Text style={styles.subtitle}>Sign in To Continue</Text>
                                <View style={styles.formGroup}>
                                    <TextInput
                                    style={styles.input}
                                    placeholder="Username"
                                    autoCapitalize="none"
                                    keyboardType="email-address"
                                    onChangeText={setUsername} 
                                    value={username} 
                                    />
                                    <TextInput
                                    style={styles.input}
                                    placeholder="Password"
                                    secureTextEntry={true}
                                    onChangeText={setPassword} 
                                    value={password} 
                                    />
                                    
                                    <TouchableOpacity style={styles.forgotPassword}>
                                        <Text style={styles.forgotPasswordText}>Forgot Password</Text>
                                    </TouchableOpacity>
                                    
                                    <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
                                        <Text style={styles.loginButtonText}>Login</Text>
                                    </TouchableOpacity>
                                    <TouchableOpacity style={styles.loginButton} onPress={handleSignup}>
                                        <Text style={styles.loginButtonText}>Sign Up</Text>
                                    </TouchableOpacity>
                                    
                                    
                                </View>
                            </View>
                        </View>
                    </View>
                </View>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
    },
    pageWrapper: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    contentWrapper: {
        width: '100%',
    },
    row: {
        flexDirection: 'row',
    },
    col: {
        flex: 1,
        alignItems: 'center',
    },
    form: {
        backgroundColor: '#fff',
        width: '80%',
        borderRadius: 10,
        padding: 20,
        elevation: 10,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
    },
    logoContainer: {
        alignItems: 'center',
        marginBottom: 20,
    },
    logo: {
        width: 100,
        height: 100,
        resizeMode: 'contain',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 10,
        textAlign: 'center',
    },
    subtitle: {
        fontSize: 18,
        color: 'grey',
        marginBottom: 20,
        textAlign: 'center',
    },
    formGroup: {
        width: '100%',
    },
    input: {
        height: 50,
        borderColor: 'gray',
        borderWidth: 1,
        marginBottom: 15,
        paddingHorizontal: 10,
        borderRadius: 5,
    },
    checkboxContainer: {
        flexDirection: 'row',
        marginBottom: 15,
        alignItems: 'center',
    },
    checkboxLabel: {
        marginLeft: 8,
        fontSize: 16,
    },
    forgotPassword: {
        alignSelf: 'flex-end',
    },
    forgotPasswordText: {
        color: '#9c27b0',
    },
    loginButton: {
        backgroundColor: '#f06292',
        padding: 15,
        borderRadius: 30,
        alignItems: 'center',
        marginTop: 10,
    },
    loginButtonText: {
        color: 'white',
        fontWeight: 'bold',
    },
});

export default LoginPage;
