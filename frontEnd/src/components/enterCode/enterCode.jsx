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
    PinInput,
    PinInputField,
    HStack,
} from "@chakra-ui/react";
import { Toaster, toast } from 'sonner';
import { verifyCodeService } from '../../service/userService.js'


export default function EnterCode({ email,code, setCode, onSuccess }) {
    const [isFetching, setIsFetching] = useState(false)
    
    const handleChange = (e) => setCode(e);

    const sendSuccess = (toastId) => {
        toast.success("Código válido", {
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

    const verifyCode = async () => {
        if(isFetching){
            return
        }

        try{
            await verifyCodeService(email,code)
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
            <h3 className='TitleSendCode'>Verifique o código enviado ao email</h3>
            <Flex
                align="center"
                justify="center"
                bg="#141414"
                px={4} 
            >
                <Box
                    p={8}
                    rounded="md"
                    maxW="xl"
                    w="100%"  
                >
                    <HStack spacing={4} mb={4} justify="center">
                        <PinInput focusBorderColor='#346E62' otp onChange={handleChange}>
                            <PinInputField color={'white'} />
                            <PinInputField color={'white'}/>
                            <PinInputField color={'white'}/>
                            <PinInputField color={'white'}/>
                            <PinInputField color={'white'}/>
                        </PinInput>
                    </HStack>

                    <Flex justify="center">
                        <Button
                            bg="#346E62"
                            _hover={{ bg: "#419181" }}
                            color="white"
                            onClick={verifyCode}
                            isLoading={isFetching}
                            loadingText="verificando código..."
                        >
                            Verificar código
                        </Button>
                    </Flex>
                </Box>
            </Flex>
        </>
    );
}