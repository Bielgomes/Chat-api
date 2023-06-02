from repository.user_repository import UserRepository
from repository.user_dto import UserDTO
from endpoints.user_vo import UserVO

class UserService():

    __user_repository = UserRepository()

    def delete_user(self, id):
        user = self.__user_repository.find(id)
        if user is None:
            raise IndexError("User not found!")
        
        self.__user_repository.delete(user)

    def find_user(self, id):
        dto : UserDTO = self.__user_repository.find(id)
        if dto is None:
            raise IndexError("User not found")
        
        return UserVO.fromDto(dto)

    def update_movie(self, id, user:UserVO):
        self.__user_repository.update(id, user.to_dto())
    

    