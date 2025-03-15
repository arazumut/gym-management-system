import bcrypt from "bcrypt";
import {getServerSession} from "next-auth/next";
import {NextApiRequest} from "next";
import {NextResponse} from "next/server";
import {options} from "../auth/[...nextauth]/options";
import {SessionUser} from "@/types";
import prisma from "@/app/libs/prismadb";
import {User} from "@prisma/client";
import {revalidatePath} from "next/cache";
import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

export async function getSession() {
    try {
        return await getServerSession(options);
    } catch (error) {
        // If there's an error, log it and return null to indicate no active session
        console.error("Error while fetching session:", error);
        return null;
    }
}

export async function GET(req: Request) {
    try {
        // Django API'sine istek gönder
        const response = await axios.get(`${API_BASE_URL}/users/`);
        
        return NextResponse.json(response.data, { status: 200 });
    } catch (error: any) {
        return NextResponse.json(
            { error: error.message || "Something went wrong" },
            { status: 500 }
        );
    }
}

export async function POST(req: Request) {
    try {
        const body = await req.json();
        
        // Django API'sine istek gönder
        const response = await axios.post(`${API_BASE_URL}/users/`, body);
        
        return NextResponse.json(response.data, { status: 201 });
    } catch (error: any) {
        return NextResponse.json(
            { error: error.message || "Something went wrong" },
            { status: 500 }
        );
    }
}

export async function PATCH(req: Request) {
    try {

        const session = await getSession();
        const sessionUser = session?.user as SessionUser;

        if (!session || !sessionUser) {
            return NextResponse.json({
                error: "unauthenticated"
            }, {
                status: 401,
            })
        }


        const body = await req.json();


        if (sessionUser?.role === 'admin' && body.trainerId && body.userId && body.trainerId !== body.userId) {

            const user = await prisma.user.findUnique({
                where: {
                    id: body.userId as string
                }
            })

            const trainer = await prisma.user.findUnique({
                where: {
                    id: body.trainerId as string
                }
            })

            if (!user || !trainer) {
                return NextResponse.json({
                    error: "No user or trainer found in the list!!!"
                }, {
                    status: 400
                })
            }

            const updateUser = await prisma.user.update({
                where: {
                    id: user.id
                }, data: {
                    trainerId: trainer.id
                }
            })

            if (!updateUser) {
                return NextResponse.json({
                    error: "Something is wrong to update the trainer"
                })
            }

            return NextResponse.json({
                message: "User updated successfully"
            }, {
                status: 201
            })
        } else if (sessionUser?.role === 'trainer' && body.trainerId && body.userId && body.trainerId !== body.userId) {
            return NextResponse.json({
                error: "You can't update the trainer"
            }, {
                status: 400
            })
        } else if (sessionUser?.role === 'user' && body.trainerId && body.userId && body.trainerId !== body.userId) {
            return NextResponse.json({
                error: "You can't update the trainer"
            }, {
                status: 400
            })
        } else {
            if (body.email) {
                return NextResponse.json({
                    error: "You can't update the email"
                }, {
                    status: 400
                })
            } else if (body.role) {
                return NextResponse.json({
                    error: "You can't update the role",
                } , {
                    status: 400
                })
            }

            const user = await prisma.user.findUnique({
                where: {
                    id: sessionUser.id
                }
            })

            if (!user) {
                return NextResponse.json({
                    error: "User not found"
                }, {
                    status: 400
                })
            }


            let hashedPassword = user.hashedPassword;

            if (body.password) {
                hashedPassword = await bcrypt.hash(body.password, 12);
            }

            const userUpdate = await prisma.user.update({
                where: {
                    id: sessionUser.id
                },
                data: {
                    name: body.name !== "" ? body.name : user.name,
                    image: body.image !== "" ? body.image : user.image,
                    age: body.age !== "" ? body.age : user.age,
                    weight: body.weight !== "" ? body.weight : user.weight,
                    height: body.height !== "" ? body.height : user.height,
                    goal: body.goal !== "" ? body.goal : user.goal,
                    level: body.level !== "" ? body.level :  user.level,
                    hashedPassword,
                    isActive: body.isActive
                }
            })

            if (!userUpdate) {
                return NextResponse.json({
                    error: "Updating failed"
                }, {
                    status: 400
                })
            }

            if (body.isActive) {
                revalidatePath("/")
            }

            return NextResponse.json({
                message: "Updated successfully"
            }, {
                status: 200
            })
        }
    } catch (err: Error | any) {
        console.error(err)
        return NextResponse.json({
            error: err.message
        }, {
            status: 500
        })
    }
}
