"use client";

import { useState, useEffect } from "react";
import toast from "react-hot-toast";
import Loader from "@/app/components/Loader/Loader";
import { useRouter } from "next/navigation";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { FieldValues, SubmitHandler, useForm } from "react-hook-form";
import axios from "axios";
import {
  Grid,
  Link,
  Avatar,
  Button,
  CssBaseline,
  TextField,
  Box,
  Typography,
  Container,
} from "@mui/material/";

const defaultTheme = createTheme();
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

export default function SignInPage() {
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const router = useRouter();

  const [testUser, setTestUser] = useState<{
    email: string;
    password: string;
  }>({
    email: "",
    password: "",
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm<FieldValues>({
    defaultValues: {
      email: "",
      password: "",
    },
  });

  // Test kullanıcı bilgilerini form alanlarına yansıt
  useEffect(() => {
    if (testUser.email) {
      setValue("email", testUser.email);
    }
    if (testUser.password) {
      setValue("password", testUser.password);
    }
  }, [testUser, setValue]);

  // Kimlik doğrulama kontrolünü kaldırdık
  // Doğrudan ana sayfaya yönlendirme yapmıyoruz

  const handleSignIn: SubmitHandler<FieldValues> = async (data) => {
    setIsSubmitting(true);
    try {
      console.log('Giriş bilgileri:', { email: data.email });
      
      // Kullanıcı bilgilerini localStorage'a kaydet (kimlik doğrulama olmadan)
      localStorage.setItem('user', JSON.stringify({
        id: 1,
        email: data.email,
        role: data.email.includes('admin') ? 'admin' : 
              data.email.includes('trainer') ? 'trainer' : 'user'
      }));
      
      toast.success("Giriş başarılı!");
      router.push('/');
    } catch (error: any) {
      console.error("Giriş hatası:", error);
      toast.error("Giriş başarısız. Lütfen bilgilerinizi kontrol edin.");
    } finally {
      setIsSubmitting(false);
    }
  };

  // Otomatik giriş butonu - doğrudan ana sayfaya gider
  const handleAutoLogin = () => {
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      email: "user@example.com",
      role: "user"
    }));
    router.push('/');
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Container component="main" maxWidth="sm">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Avatar sx={{ m: 1, backgroundColor: "secondary.main" }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Giriş Yap
          </Typography>
          
          {/* Otomatik giriş butonu */}
          <Button
            onClick={handleAutoLogin}
            fullWidth
            variant="contained"
            color="success"
            sx={{ mt: 3, mb: 2 }}
          >
            Kimlik Doğrulama Olmadan Giriş Yap
          </Button>
          
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit(handleSignIn)}
            sx={{ mt: 1 }}
          >
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="E-posta Adresi"
              autoComplete="email"
              autoFocus
              {...register("email", {
                required: "Bu alan zorunludur",
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: "Geçersiz e-posta adresi",
                },
              })}
              error={!!errors?.email?.message}
              helperText={
                errors?.email && typeof errors?.email?.message === "string"
                  ? errors?.email?.message
                  : null
              }
            />

            <TextField
              margin="normal"
              required
              fullWidth
              label="Şifre"
              type="password"
              id="password"
              autoComplete="current-password"
              {...register("password", {
                required: "Bu alan zorunludur",
              })}
              error={!!errors?.password?.message}
              helperText={
                errors?.password &&
                typeof errors?.password?.message === "string"
                  ? errors?.password?.message
                  : null
              }
            />
              <Grid container>
                    <Grid item xs ml={1}>
                        <Link href="/forgot-password" variant="body2">
                            Şifremi unuttum?
                        </Link>
                    </Grid>
                </Grid>

            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={isSubmitting}
            >
              {isSubmitting ? "Giriş yapılıyor..." : "Giriş Yap"}
            </Button>
          </Box>
        </Box>

        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 1,
            flexDirection: {
              xs: "column",
              sm: "row",
            },
          }}
        >
          <Button
            onClick={() => {
              setTestUser({
                email: "admin@example.com",
                password: "admin123",
              });
            }}
            size={"small"}
            variant="contained"
          >
            Admin Olarak Giriş
          </Button>
          <Button
            onClick={() => {
              setTestUser({
                email: "trainer@example.com",
                password: "trainer123",
              });
            }}
            size={"small"}
            variant="contained"
          >
            Eğitmen Olarak Giriş
          </Button>
          <Button
            onClick={() => {
              setTestUser({
                email: "user@example.com",
                password: "user123",
              });
            }}
            size={"small"}
            variant="contained"
          >
            Kullanıcı Olarak Giriş
          </Button>
        </Box>
      
      </Container>
    </ThemeProvider>
  );
}