import React, { useState } from 'react'
import {
  Box,
  Button,
  Flex,
  FormControl,
  FormLabel,
  Input,
  VStack,
} from "@chakra-ui/react";
import { Toaster, toast } from 'sonner';
import { updatePassword } from '../../service/userService.js';
import { useNavigate } from "react-router-dom";

export default function UpdatePassword({ email, code, onSuccess }) {
  const [isFetching, setIsFetching] = useState(false);
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const navigate = useNavigate();

  const sendError = (message, toastId) => {
    toast.error(`${message}`, {
      style: {
        background: '#8B0000',
        color: '#fff'
      },
      id: toastId,
    });
  };

  const sendSuccess = (toastId) => {
    toast.success("Senha atualizada com sucesso", {
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
  };

  const validatePassword = () => {
    if (!password || !confirmPassword) {
      sendError("Preencha os dois campos de senha");
      return false;
    }
    if (password !== confirmPassword) {
      sendError("As senhas não coincidem");
      return false;
    }
    if (password.length < 8 || password.length > 30) {
      sendError("A senha deve ter pelo menos 8 e no máximo 30 caracteres");
      return false;
    }
    return true;
  };

  const handleSubmit = async () => {
    if (!validatePassword() || isFetching) return;

    try {
      setIsFetching(true);
      await updatePassword(email, code, password); 
      sendSuccess();
      setIsFetching(false);
      await new Promise(resolve => setTimeout(resolve, 800));
      navigate("/profile")
    } catch (err) {
      sendError(err.message);
      setIsFetching(false);
    }
  };

  return (
    <>
      <Toaster position="top-right" />
      <h3 className='TitleSendCode'>Digite a nova senha</h3>
      <Flex align="center" justify="center" bg="#141414">
        <Box p={8} rounded="md" shadow="md" w="full" maxW="xl">
          <VStack spacing={4}>
            <FormControl color={'white'}>
              <FormLabel>Nova Senha</FormLabel>
              <Input
                type="password"
                name="password"
                value={password}
                bg={'#272626ff'}
                focusBorderColor='white'
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Digite sua nova senha"
              />
            </FormControl>
            <FormControl color={'white'}>
              <FormLabel>Confirmar Nova Senha</FormLabel>
              <Input
                type="password"
                name="confirmPassword"
                value={confirmPassword}
                bg={'#272626ff'}
                focusBorderColor='white'
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirme sua nova senha"
              />
            </FormControl>

            <Button
              bg="#346E62"
              _hover={{ bg: "#419181" }}
              color="white"
              width="min-content"
              onClick={handleSubmit}
              isLoading={isFetching}
              loadingText="atualizando senha..."
            >
              Alterar Senha
            </Button>
          </VStack>
        </Box>
      </Flex>
    </>
  );
}
