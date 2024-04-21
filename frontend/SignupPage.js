import React, { Component } from 'react';
import { View, Text , StyleSheet, TextInput, TouchableOpacity, Alert} from 'react-native';
import { useState } from 'react';

const SignupPage = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleSignup = () => {
        console.log('Kullanıcı Adı:', username);
        console.log('E-posta:', email);
        console.log('Parola:', password);
        console.log('Parola (Tekrar):', confirmPassword);
        Alert.alert('Registration Successful')
    };

    return (
        <View style={styles.container}>
            <View style={styles.pageWrapper}>
                <View style={styles.contentWrapper}>
                    <View style={styles.row}>
                        <View style={styles.col}>
                            <View style={styles.form}>
                                <Text style={styles.title}>Sign Up</Text>
                                <Text style={styles.subtitle}>Create an Account</Text>
                                <View style={styles.formGroup}>
                                    <TextInput
                                        style={styles.input}
                                        placeholder="Username"
                                        autoCapitalize="none"
                                        onChangeText={setUsername}
                                        value={username}
                                    />
                                    <TextInput
                                        style={styles.input}
                                        placeholder="Email"
                                        autoCapitalize="none"
                                        keyboardType="email-address"
                                        onChangeText={setEmail}
                                        value={email}
                                    />
                                    <TextInput
                                        style={styles.input}
                                        placeholder="Password"
                                        secureTextEntry={true}
                                        onChangeText={setPassword}
                                        value={password}
                                    />
                                    <TextInput
                                        style={styles.input}
                                        placeholder="Confirm Password"
                                        secureTextEntry={true}
                                        onChangeText={setConfirmPassword}
                                        value={confirmPassword}
                                    />
                                    <TouchableOpacity style={styles.signupButton} onPress={handleSignup}>
                                        <Text style={styles.signupButtonText}>Sign Up</Text>
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
    signupButton: {
        backgroundColor: '#f06292',
        padding: 15,
        borderRadius: 30,
        alignItems: 'center',
        marginTop: 10,
    },
    signupButtonText: {
        color: 'white',
        fontWeight: 'bold',
    },
});

export default SignupPage;