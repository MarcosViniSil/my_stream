import React, { useEffect, useState, useRef } from 'react'
import {
    Box,
    Button,
    Flex,
    FormControl,
    FormLabel,
    Heading,
    Input,
    VStack,
} from "@chakra-ui/react";
import { Toaster, toast } from 'sonner';
import { loginUser } from '../../service/userService.js'
import { useNavigate } from "react-router-dom";
import './login.css'

export default function Login() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });
    const [isFetching, setIsFetching] = useState(false)

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };



    const sendSuccess = (toastId) => {
        toast.success("Login realizado com sucesso", {
            style: {
                background: '#346E62',
                color: '#fff'
            },
            iconTheme: {
                primary: '#A7D1C9',
                secondary: '#fff'
            },
            id: toastId,
        });
    }

    const sendError = (message, toastId) => {
        toast.error(`${message}`, {
            style: {
                background: '#8B0000',
                color: '#fff'
            },
            id: toastId,
        });
    }

    const validateEmail = (email) => { // source: https://stackoverflow.com/posts/46181/revisions
        const isEmailValid = String(email)
            .toLowerCase()
            .match(
                /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            );
        if (!isEmailValid) {
            sendError("O formato do email informado está incorreto")
            return false
        }
        return true
    };

    const validatePassword = (password) => {
        if (password.replace(/ /g, '').length == 0) {
            sendError("A senha não pode conter apenas espaços em branco")
            return false
        }

        if (password.length < 8 || password.length > 30) {
            sendError(`A senha deve conter no mínimo 8 e no máximo 30 caracteres, tamanho atual: ${password.length}`,)
            return false
        }

        return true
    }


    const handleSubmit = async () => {

        const datas = formData
        if (!validateEmail(datas.email) || !validatePassword(datas.password)) {
            return
        }

        try {
            if (isFetching) {
                return
            }
            setIsFetching(true)
            
            const value = await loginUser(datas)
            console.log(value)
            sendSuccess()
            
            setIsFetching(false)

        } catch (err) {
            sendError(err.message)
            setIsFetching(false)
        }
    };

    return (
        <>
            <Toaster position="top-right" />
            <Flex
                color="white"
                align="center"
                justify="center"
            >
                <Box
                    bg="gray.800"
                    p={8}
                    borderRadius="xl"
                    boxShadow="lg"
                    w="lg"
                >

                    <VStack spacing={4}>
                        <FormControl>
                            <FormLabel>Email</FormLabel>
                            <Input
                                placeholder="Email"
                                name="email"
                                type="email"
                                borderColor="whiteAlpha.500"
                                value={formData.email}
                                onChange={handleChange}
                                _placeholder={{ color: "gray.400" }}
                                _hover={{ borderColor: "white" }}
                                _focus={{ borderColor: "white" }}
                                rounded="full"
                            />
                        </FormControl>

                        <FormControl>
                            <FormLabel>Senha</FormLabel>
                            <Input
                                placeholder="Senha"
                                name="password"
                                type="password"
                                borderColor="whiteAlpha.500"
                                _placeholder={{ color: "gray.400" }}
                                value={formData.password}
                                onChange={handleChange}
                                _hover={{ borderColor: "white" }}
                                _focus={{ borderColor: "white" }}
                                rounded="full"
                            />
                        </FormControl>
                        <a className='forgetPassword' href="#">Esqueci minha senha</a>
                        <Button
                            bg="#346E62"
                            _hover={{ bg: "#419181" }}
                            color="white"
                            rounded="full"
                            onClick={handleSubmit}
                            w="full"
                            mt={4}
                            isLoading={isFetching}
                            loadingText="logando..."
                        >
                            Login
                        </Button>
                    </VStack>
                </Box>
            </Flex>
        </>
    );
}