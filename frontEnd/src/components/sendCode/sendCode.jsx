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
import { sendCodeService } from '../../service/userService.js'
import './sendCode.css'


export default function SendCode({ email, setEmail, onSuccess }) {
    const [isFetching, setIsFetching] = useState(false)
    const handleChange = (e) => setEmail(e.target.value);
    const sendSuccess = (toastId) => {
        toast.success("Código enviado com sucesso", {
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

    const sendCode = async () => {
        if (!validateEmail(email) || isFetching) return;
        try{
            setIsFetching(true)
            await sendCodeService(email)
            sendSuccess()
            setIsFetching(false)
            await new Promise(resolve => setTimeout(resolve, 800));
            onSuccess()
        }catch(err){
            sendError(err.message)
            setIsFetching(false)
        }
    }

    return (
        <>
            <Toaster position="top-right" />
            <h3 className='TitleSendCode'>Digite seu email para atualizar a senha</h3>
            <Flex align="center" justify="center" bg="#141414">
                <Box p={8} rounded="md" shadow="md" w="full" maxW="xl">
                    <VStack spacing={4}>
                        <FormControl color={'white'}>
                            <FormLabel>Email</FormLabel>
                            <Input
                                type="email"
                                name="email"
                                value={email}
                                bg={'#272626ff'}
                                focusBorderColor='white'
                                onChange={handleChange}
                                placeholder="Digite seu email"
                            />
                        </FormControl>
                        <Button
                            bg="#346E62"
                            _hover={{ bg: "#419181" }}
                            color="white"
                            width="min-content"
                            onClick={sendCode}
                            isLoading={isFetching}
                            loadingText="enviando código..."
                        >
                            Enviar código de recuperação
                        </Button>
                    </VStack>
                </Box>
            </Flex>
        </>
    );
}