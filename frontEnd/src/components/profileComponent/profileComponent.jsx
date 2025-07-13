import React, { useEffect, useState } from 'react';
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
import { updateUserDatas, getUserDatasAPI } from '../../service/userService.js';
import './profileComponent.css'
import { useNavigate } from "react-router-dom";
import { Toaster, toast } from 'sonner';

export default function ProfileComponent() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({ userName: '', userEmail: '' });
  const [isFetching, setIsFetching] = useState(false);
  const [userHasLogin, setUserHasLogin] = useState(null); 

  useEffect(() => {
    const getUserDatas = async () => {
      try {
        const datas = await getUserDatasAPI();
        setFormData(datas);
        setUserHasLogin(true);
      } catch (err) {
        console.log(err);
        if (err.status === 422 || err.status === 401) {
          setUserHasLogin(false);
        } else {
          sendError(err.message);
        }
      }
    };

    getUserDatas();
  }, []);

  const sendSuccess = () => {
    toast.success("Dados atualizados com sucesso", {
      style: { background: '#346E62', color: '#fff' },
      iconTheme: { primary: '#A7D1C9', secondary: '#fff' },
    });
  };

  const sendError = (message) => {
    toast.error(`${message}`, {
      style: { background: '#8B0000', color: '#fff' },
    });
  };

  const validateName = (name) => {
    if (name.trim().length === 0) {
      sendError("O nome não pode conter apenas espaços em branco");
      return false;
    }
    if (name.length < 3 || name.length > 40) {
      sendError(`O nome deve ter entre 3 e 40 caracteres (atual: ${name.length})`);
      return false;
    }
    return true;
  };

  const validateEmail = (email) => {
    const isEmailValid = String(email).toLowerCase().match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
    if (!isEmailValid) {
      sendError("O formato do email informado está incorreto");
      return false;
    }
    return true;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const updateDatas = async () => {
    if (!validateName(formData.userName) || !validateEmail(formData.userEmail) || isFetching) {
      return;
    }

    try {
      setIsFetching(true);
      await updateUserDatas(formData);
      sendSuccess();
      navigate("/profile");
    } catch (err) {
      if (err.status === 401) {
        setUserHasLogin(false);
      }else{
        sendError(err.message);
      }
      
    } finally {
      setIsFetching(false);
    }
  };

  if (userHasLogin === null) {
    return <p style={{ color: "white", textAlign: "center" }}>Carregando...</p>;
  }

  if (!userHasLogin) {
    return (
      <div className='wrapMessageLogin'>
        <h3>Realize o login para visualizar o perfil</h3>
        <a href="/login">login</a>
      </div>
    );
  }

  return (
    <>
      <Toaster position="top-right" />
      <Flex color="white" align="center" justify="center">
        <Box bg="gray.800" p={8} borderRadius="xl" boxShadow="lg" w="lg">
          <VStack spacing={4}>
            <FormControl>
              <FormLabel>Nome</FormLabel>
              <Input
                placeholder="Nome"
                name="userName"
                borderColor="whiteAlpha.500"
                _placeholder={{ color: "gray.400" }}
                value={formData.userName}
                onChange={handleChange}
                _hover={{ borderColor: "white" }}
                _focus={{ borderColor: "white" }}
                rounded="full"
              />
            </FormControl>

            <FormControl>
              <FormLabel>Email</FormLabel>
              <Input
                placeholder="Email"
                name="userEmail"
                type="email"
                borderColor="whiteAlpha.500"
                value={formData.userEmail}
                onChange={handleChange}
                _placeholder={{ color: "gray.400" }}
                _hover={{ borderColor: "white" }}
                _focus={{ borderColor: "white" }}
                rounded="full"
              />
            </FormControl>

            <a className='changePassword' href="/password">Atualizar senha</a>

            <Button
              bg="#346E62"
              _hover={{ bg: "#419181" }}
              color="white"
              rounded="full"
              onClick={updateDatas}
              w="full"
              mt={4}
              isLoading={isFetching}
              loadingText="atualizando..."
            >
              Atualizar dados
            </Button>
          </VStack>
        </Box>
      </Flex>
    </>
  );
}
